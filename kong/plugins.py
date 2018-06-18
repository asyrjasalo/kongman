from .components import CrudComponent, ServiceEntity, KongError, KongEntity


class PluginMixin:

    def wrap(self, data):
        return Plugin.factory(self.cli, data)

    async def apply_json(self, data):
        if not isinstance(data, list):
            data = [data]
        plugins = await self.get_list()
        plugins = dict(((p['name'], p) for p in plugins))
        result = []
        for entry in data:
            name = entry.pop('name', None)
            if not name:
                raise KongError('Plugin name not specified')
            if name in plugins:
                plugin = plugins.pop(name)
                plugin = await self.update(
                    plugin['id'], name=name, **entry)
            else:
                plugin = await self.create(name=name, **entry)

            result.append(plugin.data)
        for entry in plugins.values():
            await self.delete(entry['id'])
        return result

    async def preprocess_parameters(self, params):
        await anonymous(self.cli, params)
        preprocessor = PLUGIN_PREPROCESSORS.get(params.get('name'))
        if preprocessor:
            params = await preprocessor(self.cli, params)
        return params

    async def update(self, id, **params):
        params = await self.preprocess_parameters(params)
        return await super().update(id, **params)


class Plugins(PluginMixin, CrudComponent):

    async def get_for_service(self, plugin_name, service_id):
        plugins = await self.get_list(name=plugin_name, service_id=service_id)
        if not plugins:
            raise KongError('Plugin %s not found' % plugin_name)
        return plugins[0]


class ServicePlugins(PluginMixin, ServiceEntity):

    async def create(self, skip_error=None, **params):
        params['service_id'] = self.root.id
        params = await self.preprocess_parameters(params)
        return await self.execute(
            self.url, 'post', json=params,
            wrap=self.wrap, skip_error=skip_error
        )


class RoutePlugins(PluginMixin, CrudComponent):
    """Plugins associated with a Route
    """
    def get_list(self, **params):
        url = '%s/%s' % (self.cli.url, self.name)
        params['route_id'] = self.root.id
        return self.execute(url, params=params, wrap=self.wrap_list)

    async def create(self, skip_error=None, **params):
        params['route_id'] = self.root.id
        params = await self.preprocess_parameters(params)
        return await self.execute(
            self.url, 'post', json=params,
            wrap=self.wrap, skip_error=skip_error
        )


class Plugin(KongEntity):

    @classmethod
    def factory(cls, root, data):
        if data['name'] == 'jwt':
            return JWTPlugin(root, data)
        return Plugin(root, data)


class JWTPlugin(Plugin):

    def create_consumer_jwt(self, consumer, **params):
        return self.execute(
            '%s/jwt' % consumer.url, method='POST', json=params
        )

    def get_consumer_by_jwt(self, jwt):
        return self.execute(
            '%s/jwts/%s/consumer' % (self.root.url, jwt), method='GET',
            wrap=self.root.consumers.wrap
        )

    def remove_consumer_jwt(self, consumer, jwt):
        if isinstance(consumer, dict):
            consumer = self.root.consumers.wrap(consumer)
        return self.execute('%s/jwt/%s' % (consumer.url, jwt), method='DELETE')


async def consumer_id_from_username(cli, params):
    if 'consumer_id' in params:
        c = await cli.consumers.get(params['consumer_id'])
        params['consumer_id'] = c['id']
    return params


async def anonymous(cli, params):
    if 'config' in params and 'anonymous' in params['config']:
        c = await cli.consumers.get(params['config']['anonymous'])
        params['config']['anonymous'] = c['id']
    return params


PLUGIN_PREPROCESSORS = {
    'request-termination': consumer_id_from_username
}
