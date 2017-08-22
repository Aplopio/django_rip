from model_adapter.crud_repo import CrudRepo
from rip.generic_steps.default_entity_actions import DefaultEntityActions


class ModelEntityActions(DefaultEntityActions):

    def __init__(self, model_cls, schema_cls, default_offset=0,
                 default_limit=20, crud_repo_cls=CrudRepo):
        super(ModelEntityActions, self).__init__(
            schema_cls, default_offset, default_limit)
        self.model_cls = model_cls
        self.crud_repo_cls = crud_repo_cls
        self.crud_repo = crud_repo_cls(model_cls=model_cls)

    def get_entity_list(self, request, limit, offset, **kwargs):
        return self.crud_repo.get_list(offset=offset, limit=limit, **kwargs)

    def get_entity_aggregates(self, request, **kwargs):
        return self.crud_repo.aggregates(**kwargs)

    def update_entity(self, request, entity, **update_params):
        return self.crud_repo.update(entity, **update_params)

    def delete_entity(self, request, entity):
        return self.crud_repo.delete(entity)

    def create_entity(self, request, **kwargs):
        return self.crud_repo.create(**kwargs)

    def get_entity_list_total_count(self, request, **kwargs):
        return self.crud_repo.get_count(**kwargs)
