const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    mode: 'development',
    
    entry: './static/carcassonne/js/index.js',

    output: {
        path: path.resolve('./static/carcassonne/js/'),
        filename: 'bundle.js',
    },
    
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.css$/,
                exclude: /node_modules/,
                loader: ['style-loader', 'css-loader'],
            },
            {
                test: /\.vue$/,
                exclude: /node_modules/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                    }
                }
            },
        ],
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.runtime.esm.js'
        }
    },

    devServer: {
        contentBase: 'public',
        port: 3000,
        host: 'localhost',
        historyApiFallback: true,
    },
    
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
}

