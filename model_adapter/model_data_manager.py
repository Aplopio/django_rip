from model_adapter.crud_repo import ModelRepo
from rip.generic_steps.default_data_manager import DefaultDataManager


class ModelDataManager(DefaultDataManager):

    def __init__(self, resource, model_repo_cls=ModelRepo):
        super(ModelDataManager, self).__init__(
            resource=resource)
        self.model_cls = resource._meta.model_cls
        self.model_repo_cls = model_repo_cls
        self.model_repo = model_repo_cls(model_cls=self.model_cls)

    def get_entity_list(self, request, limit, offset, **kwargs):
        return self.model_repo.get_list(offset=offset, limit=limit, **kwargs)

    def get_entity_aggregates(self, request, **kwargs):
        return self.model_repo.aggregates(**kwargs)

    def update_entity(self, request, entity, **update_params):
        return self.model_repo.update(entity, **update_params)

    def delete_entity(self, request, entity):
        return self.model_repo.delete(entity)

    def create_entity(self, request, **kwargs):
        return self.model_repo.create(**kwargs)

    def get_entity_list_total_count(self, request, **kwargs):
        return self.model_repo.get_count(**kwargs)
