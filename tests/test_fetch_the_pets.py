#!/usr/bin/env python3
"""Tests for Exercise 24: Fetch the Pets. These never touch the network."""

import os
import unittest

from src.fetch_the_pets import BASE, dog_page_urls, load_soup, pet_urls

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")

ALL_DOG_PAGES = {BASE + f"dogs-page-{n}.html" for n in range(1, 7)}
CAT_PAGES = {BASE + f"cats-page-{n}.html" for n in range(1, 5)}

# Dogs are pets 101-148 (8 per page); cats are 149-180.
DOGS_PAGE_1_PETS = {BASE + f"pet-{n}.html" for n in range(101, 109)}
CATS_PAGE_2_PETS = {BASE + f"pet-{n}.html" for n in range(157, 165)}

CARE_TIPS = BASE + "pet-care-tips.html"
OTHER_DECOYS = {
    BASE + "adoption-process.html",
    BASE + "volunteer.html",
    BASE + "donate.html",
}


def fixture(name):
    return load_soup(os.path.join(FIXTURES, name))


class UrlChecks(unittest.TestCase):
    """Shared checks that turn common mistakes into plain-English failures."""

    def check_list(self, result, name):
        self.assertIsNotNone(
            result,
            msg=f"{name} returned None. Did you forget the return statement?",
        )
        self.assertIsInstance(
            result,
            list,
            msg=f"{name} should return a list, but it returned a "
            f"{type(result).__name__}. If you built a set, turn it into a list "
            "before returning it.",
        )

    def check_full_urls(self, result, name):
        short = [u for u in result if not str(u).startswith("https://")]
        self.assertEqual(
            short,
            [],
            msg=f"{name}: these should be full URLs starting with https://, but "
            f"some are just the end of the link: {short[:3]}. Put BASE in front "
            "of each href.",
        )

    def check_no_duplicates(self, result, name):
        repeats = sorted({u for u in result if result.count(u) > 1})
        self.assertEqual(
            repeats,
            [],
            msg=f"{name}: a URL appears twice in your list: {repeats[:3]}. Some "
            "links show up more than once on the page; keep each URL only once.",
        )

    def check_no_cat_pages(self, result, name):
        cats = sorted(set(result) & CAT_PAGES)
        self.assertEqual(
            cats,
            [],
            msg=f"{name}: a cat page got in: {cats}. Every page links to the "
            "cat pages too, but you only want the dog pages.",
        )

    def check_no_care_tips(self, result, name):
        self.assertNotIn(
            CARE_TIPS,
            result,
            msg=f"{name}: pet-care-tips isn't a pet. It starts with 'pet-', but "
            "a real pet page has an ID number.",
        )

    def check_no_other_decoys(self, result, name):
        decoys = sorted(set(result) & OTHER_DECOYS)
        self.assertEqual(
            decoys,
            [],
            msg=f"{name}: a decoy link from the menu got in: {decoys}.",
        )


class TestDogPageUrlsOnDogsPage1(UrlChecks):
    """dog_page_urls(soup) on dogs-page-1."""

    def setUp(self):
        self.result = dog_page_urls(fixture("dogs-page-1.html"))

    def test_returns_a_list(self):
        self.check_list(self.result, "dog_page_urls")

    def test_full_urls(self):
        self.check_list(self.result, "dog_page_urls")
        self.check_full_urls(self.result, "dog_page_urls")

    def test_no_duplicates(self):
        self.check_list(self.result, "dog_page_urls")
        self.check_no_duplicates(self.result, "dog_page_urls")

    def test_no_cat_pages(self):
        self.check_list(self.result, "dog_page_urls")
        self.check_no_cat_pages(self.result, "dog_page_urls")

    def test_no_decoys(self):
        self.check_list(self.result, "dog_page_urls")
        self.check_no_care_tips(self.result, "dog_page_urls")
        self.check_no_other_decoys(self.result, "dog_page_urls")
        pets = sorted(u for u in self.result if "pet-" in str(u))
        self.assertEqual(
            pets,
            [],
            msg=f"dog_page_urls: a pet's page got in: {pets[:3]}. This function "
            "should only collect the dog list pages.",
        )

    def test_finds_6_pages(self):
        self.check_list(self.result, "dog_page_urls")
        self.assertEqual(
            len(self.result),
            6,
            msg=f"dog_page_urls found {len(self.result)} URLs on dogs-page-1, "
            "but there are 6 dog pages.",
        )

    def test_exact_pages(self):
        self.check_list(self.result, "dog_page_urls")
        missing = sorted(ALL_DOG_PAGES - set(self.result))
        extra = sorted(set(self.result) - ALL_DOG_PAGES)
        self.assertEqual(
            set(self.result),
            ALL_DOG_PAGES,
            msg="dog_page_urls on dogs-page-1 should be exactly the 6 dog pages. "
            f"Missing: {missing[:3]}  Should not be there: {extra[:3]}",
        )


class TestDogPageUrlsOnDogsPage6(UrlChecks):
    """dog_page_urls(soup) on dogs-page-6, the last page, which has no Next link."""

    def setUp(self):
        self.result = dog_page_urls(fixture("dogs-page-6.html"))

    def test_still_finds_all_6_pages(self):
        self.check_list(self.result, "dog_page_urls")
        missing = sorted(ALL_DOG_PAGES - set(self.result))
        self.assertEqual(
            missing,
            [],
            msg=f"dog_page_urls on dogs-page-6 is missing {missing[:3]}. The last "
            "page has no 'Next' link, so don't rely on it: every page number is "
            "listed at the bottom of every page.",
        )
        self.check_full_urls(self.result, "dog_page_urls")
        self.check_no_duplicates(self.result, "dog_page_urls")
        self.check_no_cat_pages(self.result, "dog_page_urls")
        self.assertEqual(
            len(self.result),
            6,
            msg=f"dog_page_urls found {len(self.result)} URLs on dogs-page-6, "
            "but there are 6 dog pages.",
        )


class TestPetUrlsOnDogsPage1(UrlChecks):
    """pet_urls(soup) on dogs-page-1."""

    def setUp(self):
        self.result = pet_urls(fixture("dogs-page-1.html"))

    def test_returns_a_list(self):
        self.check_list(self.result, "pet_urls")

    def test_full_urls(self):
        self.check_list(self.result, "pet_urls")
        self.check_full_urls(self.result, "pet_urls")

    def test_no_duplicates(self):
        self.check_list(self.result, "pet_urls")
        self.check_no_duplicates(self.result, "pet_urls")

    def test_no_care_tips(self):
        self.check_list(self.result, "pet_urls")
        self.check_no_care_tips(self.result, "pet_urls")

    def test_no_list_pages_or_decoys(self):
        self.check_list(self.result, "pet_urls")
        self.check_no_other_decoys(self.result, "pet_urls")
        pages = sorted(set(self.result) & (ALL_DOG_PAGES | CAT_PAGES))
        self.assertEqual(
            pages,
            [],
            msg=f"pet_urls: a list page got in: {pages[:3]}. pet_urls should "
            "only collect the pets' own pages.",
        )

    def test_finds_8_pets(self):
        self.check_list(self.result, "pet_urls")
        self.assertEqual(
            len(self.result),
            8,
            msg=f"pet_urls found {len(self.result)} URLs on dogs-page-1, but "
            "each page lists 8 pets.",
        )

    def test_exact_pets(self):
        self.check_list(self.result, "pet_urls")
        missing = sorted(DOGS_PAGE_1_PETS - set(self.result))
        extra = sorted(set(self.result) - DOGS_PAGE_1_PETS)
        self.assertEqual(
            set(self.result),
            DOGS_PAGE_1_PETS,
            msg="pet_urls on dogs-page-1 should be exactly its 8 pets. "
            f"Missing: {missing[:3]}  Should not be there: {extra[:3]}",
        )


class TestPetUrlsOnCatsPage2(UrlChecks):
    """pet_urls(soup) on cats-page-2: it has to work on a cat page too."""

    def setUp(self):
        self.result = pet_urls(fixture("cats-page-2.html"))

    def test_finds_the_8_cats(self):
        self.check_list(self.result, "pet_urls")
        self.check_full_urls(self.result, "pet_urls")
        self.check_no_duplicates(self.result, "pet_urls")
        self.check_no_care_tips(self.result, "pet_urls")
        self.assertEqual(
            len(self.result),
            8,
            msg=f"pet_urls found {len(self.result)} URLs on cats-page-2, but "
            "each page lists 8 pets. pet_urls has to work on cat pages too.",
        )
        missing = sorted(CATS_PAGE_2_PETS - set(self.result))
        extra = sorted(set(self.result) - CATS_PAGE_2_PETS)
        self.assertEqual(
            set(self.result),
            CATS_PAGE_2_PETS,
            msg="pet_urls on cats-page-2 should be exactly the 8 cats on that "
            "page. Make sure nothing in your code only works for dogs. "
            f"Missing: {missing[:3]}  Should not be there: {extra[:3]}",
        )


if __name__ == "__main__":
    unittest.main()
