var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')

let resolve = (dir) => {
    return path.join(__dirname, dir)
}

module.exports = {
    mode: 'none',

    entry: {
        '../smallbusiness-module-company/smallbusiness/module/company/static/build/application': resolve('./application/entry/application.js'),
        '../smallbusiness-module-company/smallbusiness/module/company/static/build/css': resolve('./application/style/scss/layout.scss')
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
            '@style': resolve('./application/style/scss'),
            '@application': resolve('./application'),
            '@component': resolve('./application/component'),
            '@': resolve('.')
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
            { from: resolve('node_modules/bootstrap/dist/css/bootstrap.css'), to: '../smallbusiness-module-company/smallbusiness/module/company/static/build/css' },
            { from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css'), to: '../smallbusiness-module-company/smallbusiness/module/company/static/build/css' },
            { from: resolve('node_modules/@fortawesome/fontawesome-free'), to: "../smallbusiness-module-company/smallbusiness/module/company/static/build/css/font-awesome" }
        ])
    ]
}
