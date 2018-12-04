var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')

let resolve = (dir) => {
    return path.join(__dirname, dir)
}

module.exports = {
    mode: 'none',

    entry: {
        'homebusiness/static/_build/application': resolve('assets/application/application.js'),
        'homebusiness/static/_build/css': resolve('assets/scss/layout.scss')
    },

    devtool: 'source-map',

    output: {
        path: resolve("."),
        publicPath: '/static'
    },

    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            'vue$': 'vue/dist/vue.js',
            '@style': resolve('assets/scss'),
            '@application': resolve('assets/application'),
            '@component': resolve('assets/application/component'),
            '@': resolve('assets')
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
            { from: resolve('node_modules/bootstrap/dist/css/bootstrap.css'), to: './homebusiness/static/_build/css' },
            { from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css'), to: './homebusiness/static/_build/css' },
            { from: resolve('node_modules/@fortawesome/fontawesome-free'), to: "./homebusiness/static/_build/css/font-awesome" }
        ])
    ]
}
