# Get data by download files & for rujia
- change settings.py
    ```
    ITEM_PIPELINES : {
    'jigsaw.pipelines.StaffPipeline': 300,
    }
    ```

- run
    ```
    scrapy crawl staff
    ```

- result
    ```
    cd /Users/twer/work/pjhu/crawler/scrapytutorial/jigsaw
    python jigsaw/spiders/merge.py
    ```

# Get data by search
- change cookie

- change settings.py
    ```
    ITEM_PIPELINES : {
    'jigsaw.pipelines.JigsawPipeline': 300,
    }
    ```

- run
    ```
    cd /Users/twer/work/pjhu/crawler/scrapytutorial/jigsaw
    scrapy crawl jigsaw
    ```
