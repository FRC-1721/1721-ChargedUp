# FRC 1721 Dashboard

## Getting Started

-   Make sure you have sed installed
-   Make sure Robot Simulation is running
-   Install npm

Install deps

```shell
npm ci
```

Build webpage

```shell
npm run build

# Or..
make build
```

Build automatically on file changed in src/ (requires 'entr', `paru -S entr` `pamac install entr`)

```
make dev
```

Run webpage

```shell
npm run run

# Or..
make run
```

`npm run run` can be left running when you run `npm run build` again, and does not need to be run again to update the webpage
