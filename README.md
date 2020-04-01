# wikipedia_dark_theme
Native dark theme for Wikipedia

## Usage

- Download `/css/main.css`
- Go to Wikipedia > Settings > UI > Custom CSS > Upload the file
- There should be several errors. That doesn't matter, you can ignore it. The root of error is sass compiler that add sass info into the file header.
- Press save

## Limitations

- Several table cells has inlined css so it can not be overrided by css file.
- Several icons will be barely visible (I'll try to fix it asap)

## Developing

- Clone the repo
- Run `npm run scss`