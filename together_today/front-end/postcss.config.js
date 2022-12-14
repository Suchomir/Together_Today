const isProduction = process.env.NODE_ENV === "production";

const config = {
  plugins: [
    require("postcss-omit-import-tilde"),
    require("postcss-import"),
    require("tailwindcss")("./tailwind.config.js"),
    require("postcss-nested"),
    require("postcss-font-magician")({
      formats: "local woff ttf",
      hosted: ["../dist/fonts", "/static/fonts/"],
    }),
  ],
};

if (isProduction) {
  config.plugins.push(
    ...[require("autoprefixer"), require("cssnano", { preset: "default" })]
  );
}

module.exports = config;
