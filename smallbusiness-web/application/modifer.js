// In generally for conver bolean values
// from int and int to boolean

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

        if (!_.isUndefined(modificatorObject) && _.isFunction(modificatorObject.modificator)) {
            return modificatorObject.modificator(data)
        }

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


registry.register(({direction, url, method}) => {
    return direction === 'response' && /\/api\/user/.test(url) && method === 'get'
}, request => {

    if (_.isArray(request)) {
        var users = request
    } else {
        var users = [request]
    }

    _.forEach(users, user => {
        user.sudo = Boolean(user.sudo)

        if (_.isArray(user.permissions)) {
            user.permissions = user.permissions.map(permission => {
                return _.merge(permission, {
                    'create': Boolean(permission.create),
                    'read': Boolean(permission.read),
                    'update': Boolean(permission.update),
                    'delete': Boolean(permission.delete),
                })
            })
        }
    })

    return request
})


export {registry}
