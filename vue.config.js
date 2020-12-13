// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  outputDir: "dist",
  devServer: {
    proxy: {
      "/api*": {
        // Forward frontend dev server request for /api to flask dev server
        target: "http://localhost:5000/",
      },
    },
  },
};
