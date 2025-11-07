# Nuget packages scraper

Your company is too big and old to properly handle nuget certificates on different operating systems?
You could download them manually one by one, or you could use this tool to scrape them all at once!

This tool assumes <https://www.nuget.org> is not protected by a corporate firewall or proxy.

## How this works?

This tool scans build logs from running `dotnet restore` for missing nuget packages and downloads them from nuget.org.
Tries to download correct version, but if not found, downloads ALL versions of the package.
Leave this tool running for 10 minutes, it will continously scan for new missing packages in the logs and download them to a local folder.

## One-Time Setup

Create a folder to store your downloaded NuGet packages:

```bash
mkdir -p ~/localnugetpackages
```

Or create it in a location of your choice:

```bash
mkdir -p /path/to/your/localnugetpackages
```

## Usage

```bash
pip install -r requirements.txt &&
python main.py --log-file PATH_TO_YOUR_BUILD_LOG_FILE --output-folder PATH_TO_YOUR_OUTPUT_FOLDER
```
