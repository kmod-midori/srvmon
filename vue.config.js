module.exports = {
  outputDir: "dist",
  devServer: {
    proxy: {
      "/api*": {
        target: "http://localhost:5000/",
        ws: true,
        changeOrigin: true,
      },
    },
  },
  transpileDependencies: ["vuetify"],
};
