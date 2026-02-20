/** @type {import("stylelint").Config} */
export default {
  "extends": [
    "stylelint-config-standard",
    "stylelint-config-html/svelte"
  ],
  "ignoreFiles": ["src/paraglide/**", "src/generated/**","src/locales/**","**/*.ts"],
  "overrides": [
    {
      "files": ["**/*.svelte"],
      "customSyntax": "postcss-html"
    }
  ],
  "rules": {
    "selector-pseudo-class-no-unknown": [
      true,
      { "ignorePseudoClasses": ["global"] }
    ]
  }
};