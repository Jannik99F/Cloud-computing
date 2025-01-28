from sqlmodel import SQLModel

class BaseModel(SQLModel, table=False):
    def append_relation(self, model_dict, relation_name):
        relation = getattr(self, relation_name, None)
        if relation is not None:
            if isinstance(relation, list):
                model_dict[relation_name] = [item.dict() for item in relation]
            else:
                model_dict[relation_name] = relation.dict()
        return model_dict

    def load_relations(self, relations_to_load=None):
        model_dict = self.dict()

        if relations_to_load:
            for relation_name in relations_to_load:
                model_dict = self.append_relation(model_dict, relation_name)

        return model_dict