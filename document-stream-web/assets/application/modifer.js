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
    return direction === 'request' && /\/api\/account\/\d/.test(url) && _.includes(['put', 'post'], method)
}, account => {
    
    if (_.isDate(account.date)) {
        account.date = account.date.getTime()
    }
    
    return account
})


registry.register(({direction, url, method}) => {
    return direction === 'response' && /\/api\/account\/\d/.test(url) && _.includes(['get'], method)
}, account => {
    
    if (_.isNumber(account.date)) {
        account.date = new Date(account.date)
    }
    
    return account
})

export {registry}
