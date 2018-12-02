import _ from 'lodash'


class ModiferRegistry {
    constructor () {
        this._registry = []
    }

    register(predicat, modificator) {
        this._registry.push({predicat, modificator})
    }

    modify(context, data) {
        const modificatorObject = _.chain(this._registry)
            .filter(({predicat, modificator}) => predicat(context))
            .head()
            .value()

        try {
            return _.isFunction(modificatorObject.modificator) ? modificatorObject.modificator(data) : data
        } catch (_error) {}

        return data
    }

}


const registry = new ModiferRegistry()


registry.register(({direction, url, method}) => {
    return direction === 'request' && /\/api\/account/.test(url) && _.includes(['put', 'post'], method)
}, request => {
    if (_.isDate(request.date)) {
        request.date = request.date.getTime()
    }
    
    return request
})


registry.register(({direction, url, method}) => {
    return direction === 'response' && /\/api\/account/.test(url) && method === 'get'
}, response => {

    function setupDate(account) {
        if (_.isNumber(account.date)) {
            account.date = new Date(account.date)
        }
    }

    if (_.isArray(response)) {
        _.each(response, account => {
            setupDate(account)
        })
    } else {
        setupDate(response)
    }
    
    return response
})

export {registry}
