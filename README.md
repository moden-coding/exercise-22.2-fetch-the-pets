# Exercise 24: Fetch the Pets

## The goal

Collect every dog page, and every pet on a page, so a later assignment can
visit them all.

## The site

https://moden-coding.github.io/scrape-practice-site/shelter/dogs-page-1.html

Open it and Inspect the links at the top and bottom of the page.

## What to write

In `src/fetch_the_pets.py`:

- `dog_page_urls(soup)`: the full URLs of all the dog pages. Expect **6**.
- `pet_urls(soup)`: the full URLs of the pet detail pages on this page. Expect **8**. It has to work on a cat page too.

Both return a list with no duplicates. Leave the toolkit at the top alone.

## Watch out for

- This page links to cat pages too.
- Some links appear twice.
- Not every link that starts with pet- is a pet.

## Run it

```
python src/fetch_the_pets.py
python -m unittest discover
```

## Done when

All tests pass and `main()` prints 6 pages and 8 pets.
