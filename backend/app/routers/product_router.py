from sqlmodel import Session, SQLModel, select
from models.product import Product
from utils.azure_storage import AzureBlobStorage
from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse
import json

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_all_products(session: Session = Depends(get_session)):
    statement = select(Product)
    products = session.exec(statement).all()

    products = [product.load_relations(relations_to_load=["variances"]) for product in products]

    session.close()

    return products

@router.get("/{product_id}")
def get_product_by_id(product_id: int, session: Session = Depends(get_session)):
    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    product = product.load_relations(relations_to_load=["variances"])

    session.close()

    return product

@router.post("/")
async def create_product(request: Request, session: Session = Depends(get_session)):
    product_data = await request.json()

    for product in product_data:
        base_price = product.get("base_price")
        name = product.get("name")
        furniture_type = product.get("furniture_type")
        product_type = product.get("product_type")
        height = product.get("height")
        width = product.get("width")
        depth = product.get("depth")
        image_url = product.get("image_url")  # Get image_url if provided

        new_product = Product(
            base_price=base_price,
            name=name,
            furniture_type=furniture_type,
            product_type=product_type,
            height=height,
            width=width,
            depth=depth,
            image_url=image_url,  # Add image_url to product
        )
        session.add(new_product)
        session.commit()

        session.refresh(new_product)

        new_product = new_product.load_relations(relations_to_load=["variances"])

    session.close()

    return { "message": str(len(product_data)) + " products were created successfully." }

@router.patch("/{product_id}")
async def update_product(product_id: int, request: Request, session: Session = Depends(get_session)):
    data = await request.json()

    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    for key, value in data.items():
        if value is not None and hasattr(product, key):
            setattr(product, key, value)

    session.add(product)
    session.commit()

    session.refresh(product)

    product = product.load_relations(relations_to_load=["variances"])

    session.close()

    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    session.delete(product)
    session.commit()

    session.close()

    return {"message": "Product deleted successfully."}

@router.delete("/")
def nuke_products(session: Session = Depends(get_session)):
    statement = select(Product)
    products = session.exec(statement).all()

    for product in products:
        session.delete(product)
        session.commit()
    
    session.close()

    return {"message": "All products have been deleted."}


@router.post("/{product_id}/upload-image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # Check if product exists
    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    # Read the file content
    image_data = await file.read()
    
    # Get the file extension
    file_ext = file.filename.split(".")[-1].lower()
    
    # Define content type based on extension
    content_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    content_type = content_type_map.get(file_ext, "image/jpeg")
    
    # Create a filename with product ID
    filename = f"product_{product_id}_{file.filename}"
    
    try:
        # Upload to Azure Blob Storage
        storage = AzureBlobStorage()
        
        # If product already has an image, delete it first
        if product.image_url:
            storage.delete_image(product.image_url)
        
        # Upload new image
        image_url = storage.upload_image(
            image_data, 
            filename=filename,
            content_type=content_type
        )
        
        # Update product with image URL
        product.image_url = image_url
        session.add(product)
        session.commit()
        session.refresh(product)
        
        product_dict = product.load_relations(relations_to_load=["variances"])
        
        session.close()
        
        return product_dict
        
    except Exception as e:
        session.close()
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")
