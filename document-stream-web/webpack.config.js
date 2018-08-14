var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')

let resolve = (dir) => {
    return path.join(__dirname, dir)
}

module.exports = {
    mode: 'none',

    entry: {
        'static/_build/application': resolve('assets/application/application.js')
    },

    output: {
        path: resolve("."),
        publicPath: '/static'
    },

    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            'vue$': 'vue/dist/vue.js',
            '@style': resolve('assets/scss'),
            '@application': resolve('assets/application')
        }
    },

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [resolve('application')],
                query: {
                    presets: 'es2015',
                    plugins: ['transform-es2015-destructuring', 'transform-object-rest-spread']
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.scss$/,
                use: ["style-loader", "css-loader", "sass-loader"]
            }
        ]
    },

    plugins: [
        new CopyWebpackPlugin([
            { from: resolve('node_modules/mini.css/dist/mini-default.css'), to: './static/_build/css' }
        ])
    ]
}
