from sqlmodel import SQLModel

class BaseModel(SQLModel, table=False):
    def load_relations(self, relations_to_load=None):
        model_dict = self.dict()

        if relations_to_load:
            for relation_name in relations_to_load:
                relation_parts = relation_name.split('.')
                model_dict = self._load_nested_relation(model_dict, relation_parts)

        return model_dict

    def _load_nested_relation(self, model_dict, relation_parts):
        relation_name = relation_parts[0]
        relation = getattr(self, relation_name, None)

        if relation:
            if isinstance(relation, list):
                model_dict[relation_name] = [
                    item.
                    load_relations(['.'.join(relation_parts[1:])]) if relation_parts[1:] else item.dict()
                    for item in relation
                ]
            else:
                model_dict[relation_name] = (
                    relation
                    .load_relations(['.'.join(relation_parts[1:])])) if relation_parts[1:] else relation.dict()

        return model_dict
