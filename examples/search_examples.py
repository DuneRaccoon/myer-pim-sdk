# examples/search_examples.py

"""
Comprehensive examples demonstrating the search functionality of the Myer PIM SDK.

This file shows how to use the various search methods and filters available
for products and product models in the Akeneo API.
"""

import asyncio
from datetime import datetime, timedelta
from myer_pim_sdk import (
    AkeneoClient, 
    AkeneoAsyncClient,
    SearchBuilder,
    FilterBuilder,
    ProductPropertyFilter,
    ProductModelPropertyFilter,
    AttributeFilter,
    ListOperator,
    TextOperator,
    CategoryOperator,
    CompletenessOperator
)


def basic_search_examples():
    """Examples of basic search functionality."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("=== Basic Search Examples ===")
    
    # 1. Find enabled products
    print("\\n1. Finding enabled products...")
    enabled_products = client.products.find_enabled()
    print(f"Found {len(enabled_products)} enabled products")
    
    # 2. Find products in specific categories
    print("\\n2. Finding products in winter collection...")
    winter_products = client.products.find_in_categories(["winter_collection"])
    print(f"Found {len(winter_products)} products in winter collection")
    
    # 3. Find products by family
    print("\\n3. Finding products in clothing family...")
    clothing_products = client.products.find_by_family(["clothing"])
    print(f"Found {len(clothing_products)} clothing products")
    
    # 4. Find incomplete products
    print("\\n4. Finding incomplete products...")
    incomplete_products = client.products.find_incomplete("ecommerce", threshold=80)
    print(f"Found {len(incomplete_products)} products less than 80% complete")
    
    # 5. Find recently updated products
    print("\\n5. Finding recently updated products...")
    recent_products = client.products.find_recently_updated(7)  # Last 7 days
    print(f"Found {len(recent_products)} products updated in last 7 days")


def advanced_search_examples():
    """Examples of advanced search functionality using SearchBuilder."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Advanced Search Examples ===")
    
    # 1. Complex search with multiple filters
    print("\\n1. Complex search with multiple filters...")
    products = client.products.search_with_builder(
        lambda f: f.enabled(True)
                  .categories(["winter_collection"], "IN")
                  .family(["clothing"])
                  .completeness(80, "ecommerce", ">")
                  .updated(30, "SINCE LAST N DAYS")
    )
    print(f"Found {len(products)} products matching complex criteria")
    
    # 2. Using SearchBuilder directly
    print("\\n2. Using SearchBuilder directly...")
    builder = (SearchBuilder()
               .filters(lambda f: f.enabled(True).family(["shoes"]))
               .search_locale("en_US")
               .search_scope("ecommerce")
               .pagination(page=1, limit=50))
    
    products = client.products.search_with_builder(builder, paginated=True)
    print(f"Found {len(products.items)} shoes on page {products.current_page}")
    print(f"Has next page: {products.has_next}")
    
    # 3. Attribute-based search
    print("\\n3. Searching by attribute values...")
    products = client.products.search_with_builder(
        lambda f: f.attribute_text("description", "premium", "CONTAINS", "en_US", "ecommerce")
                  .attribute_select("color", ["red", "blue"], "IN")
    )
    print(f"Found {len(products)} products with 'premium' in description and red/blue color")
    
    # 4. Date-based search
    print("\\n4. Date-based search...")
    cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    products = client.products.search_with_builder(
        lambda f: f.created(cutoff_date, ">")
    )
    print(f"Found {len(products)} products created in last 30 days")


def product_model_search_examples():
    """Examples of product model search functionality."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Product Model Search Examples ===")
    
    # 1. Find root product models
    print("\\n1. Finding root product models...")
    root_models = client.product_models.find_root_models()
    print(f"Found {len(root_models)} root product models")
    
    # 2. Find sub product models
    print("\\n2. Finding sub product models...")
    sub_models = client.product_models.find_sub_models()
    print(f"Found {len(sub_models)} sub product models")
    
    # 3. Find complete product models
    print("\\n3. Finding complete product models...")
    complete_models = client.product_models.find_complete("ecommerce", locale="en_US")
    print(f"Found {len(complete_models)} complete product models")
    
    # 4. Find models by family
    print("\\n4. Finding product models by family...")
    clothing_models = client.product_models.find_by_family(["clothing"])
    print(f"Found {len(clothing_models)} clothing product models")
    
    # 5. Myer-specific: Find models for enrichment
    print("\\n5. Finding models ready for image enrichment...")
    models_for_enrichment = client.product_models.find_for_enrichment("image", 10)
    print(f"Found {len(models_for_enrichment)} models ready for image enrichment")


def myer_specific_workflows():
    """Myer-specific search workflows for enrichment processes."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Myer-Specific Workflows ===")
    
    # 1. Find products ready for image enrichment
    print("\\n1. Finding products ready for image enrichment...")
    image_ready = client.product_models.search_with_builder(
        lambda f: f.attribute_number("image_status", 10)  # Status 10 = ready
    )
    print(f"Found {len(image_ready)} product models ready for image enrichment")
    
    # 2. Find products with copy enrichment complete
    print("\\n2. Finding products with copy enrichment complete...")
    copy_complete = client.product_models.search_with_builder(
        lambda f: f.attribute_number("copy_status", 20)  # Status 20 = complete
    )
    print(f"Found {len(copy_complete)} product models with copy enrichment complete")
    
    # 3. Find incomplete products in specific supplier categories
    print("\\n3. Finding incomplete products from specific suppliers...")
    incomplete_supplier_products = client.products.search_with_builder(
        lambda f: f.categories(["supplier_category_1", "supplier_category_2"], "IN")
                  .completeness(90, "ecommerce", "<")
                  .enabled(True)
    )
    print(f"Found {len(incomplete_supplier_products)} incomplete products from suppliers")
    
    # 4. Find products with quality issues
    print("\\n4. Finding products with quality scores below B...")
    quality_issues = client.products.find_with_quality_score(["C", "D", "E"], "ecommerce", "en_US")
    print(f"Found {len(quality_issues)} products with quality issues")
    
    # 5. Complex enrichment workflow search
    print("\\n5. Complex enrichment workflow search...")
    enrichment_candidates = client.product_models.search_with_builder(
        lambda f: f.attribute_number("image_status", 10)  # Ready for images
                  .attribute_empty("description", True, "en_US", "ecommerce")  # No description
                  .family(["clothing", "shoes", "accessories"])  # Specific families
                  .categories(["new_arrivals"], "IN")  # In new arrivals
    )
    print(f"Found {len(enrichment_candidates)} models needing comprehensive enrichment")


def raw_search_examples():
    """Examples using raw search criteria (for advanced users)."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Raw Search Examples ===")
    
    # 1. Raw search criteria
    print("\\n1. Using raw search criteria...")
    search_criteria = {
        "enabled": [{"operator": "=", "value": True}],
        "family": [{"operator": "IN", "value": ["clothing"]}],
        "categories": [{"operator": "IN", "value": ["winter_collection"]}],
        "completeness": [{"operator": ">", "value": 80, "scope": "ecommerce"}]
    }
    products = client.products.search(search_criteria)
    print(f"Found {len(products)} products using raw search")
    
    # 2. Raw filter with SearchBuilder
    print("\\n2. Mixing raw filters with SearchBuilder...")
    builder = (SearchBuilder()
               .raw_filter("enabled", "=", True)
               .raw_filter("categories", "IN", ["winter_collection"])
               .raw_filter("description", "CONTAINS", "premium", "en_US", "ecommerce"))
    
    products = client.products.search_with_builder(builder)
    print(f"Found {len(products)} products using mixed approach")


async def async_search_examples():
    """Examples of asynchronous search functionality."""
    
    client = AkeneoAsyncClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    try:
        print("\\n=== Async Search Examples ===")
        
        # 1. Async enabled products search
        print("\\n1. Finding enabled products asynchronously...")
        enabled_products = await client.products.find_enabled_async()
        print(f"Found {len(enabled_products)} enabled products")
        
        # 2. Async complex search
        print("\\n2. Complex async search...")
        products = await client.products.search_with_builder_async(
            lambda f: f.enabled(True)
                      .family(["clothing"])
                      .completeness(80, "ecommerce", ">"),
            paginated=True
        )
        print(f"Found {len(products.items)} products on page {products.current_page}")
        
        # 3. Async product model search
        print("\\n3. Finding product models asynchronously...")
        models = await client.product_models.find_by_family_async(["shoes"])
        print(f"Found {len(models)} shoe product models")
        
        # 4. Parallel async searches
        print("\\n4. Running parallel async searches...")
        results = await asyncio.gather(
            client.products.find_enabled_async(categories=["winter_collection"]),
            client.products.find_incomplete_async("ecommerce", 90),
            client.product_models.find_root_models_async()
        )
        
        enabled_winter, incomplete, root_models = results
        print(f"Parallel results: {len(enabled_winter)} winter products, "
              f"{len(incomplete)} incomplete products, {len(root_models)} root models")
        
    finally:
        await client.close()


def pagination_examples():
    """Examples of pagination with search."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Pagination Examples ===")
    
    # 1. Basic pagination
    print("\\n1. Basic pagination...")
    page1 = client.products.search_with_builder(
        lambda f: f.enabled(True),
        paginated=True
    )
    print(f"Page 1: {len(page1.items)} items, has_next: {page1.has_next}")
    
    # 2. Manual pagination
    print("\\n2. Manual pagination...")
    builder = SearchBuilder().filters(lambda f: f.family(["clothing"])).limit(20)
    
    page_num = 1
    total_found = 0
    
    while True:
        builder.page(page_num)
        page = client.products.search_with_builder(builder, paginated=True)
        
        total_found += len(page.items)
        print(f"Page {page_num}: {len(page.items)} items")
        
        if not page.has_next or page_num >= 3:  # Limit to 3 pages for example
            break
        page_num += 1
    
    print(f"Total found across pages: {total_found} items")
    
    # 3. Iterator-style pagination (using the base paginate method)
    print("\\n3. Iterator-style pagination...")
    count = 0
    for product in client.products.paginate(family=["shoes"], limit=10):
        count += 1
        if count >= 50:  # Limit for example
            break
    print(f"Processed {count} products using iterator")


def filter_combination_examples():
    """Examples of combining different types of filters."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Filter Combination Examples ===")
    
    # 1. Property + Attribute filters
    print("\\n1. Combining property and attribute filters...")
    products = client.products.search_with_builder(
        lambda f: f.enabled(True)  # Property filter
                  .family(["clothing"])  # Property filter
                  .attribute_text("brand", "Nike", "=")  # Attribute filter
                  .attribute_select("color", ["red", "blue"], "IN")  # Attribute filter
    )
    print(f"Found {len(products)} Nike clothing products in red/blue")
    
    # 2. Multiple conditions on same property
    print("\\n2. Multiple conditions on same property...")
    products = client.products.search_with_builder(
        lambda f: f.categories(["winter_collection"], "IN")
                  .categories(["clearance"], "NOT IN")  # Exclude clearance
    )
    print(f"Found {len(products)} winter products not on clearance")
    
    # 3. Date range filters
    print("\\n3. Date range filters...")
    start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    products = client.products.search_with_builder(
        lambda f: f.created([start_date, end_date], "BETWEEN")
                  .updated(7, "SINCE LAST N DAYS")  # But updated recently
    )
    print(f"Found {len(products)} products created 30-60 days ago but updated recently")
    
    # 4. Completeness with locales
    print("\\n4. Completeness with specific locales...")
    products = client.products.search_with_builder(
        lambda f: f.completeness(100, "ecommerce", "GREATER OR EQUALS THAN ON ALL LOCALES", 
                                ["en_US", "fr_FR"])
    )
    print(f"Found {len(products)} products 100% complete in English and French")


if __name__ == "__main__":
    """
    Run all examples. In practice, you would run these individually
    and replace the client credentials with your actual values.
    """
    
    print("Myer PIM SDK - Search Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run:
    
    # basic_search_examples()
    # advanced_search_examples()
    # product_model_search_examples()
    # myer_specific_workflows()
    # raw_search_examples()
    # pagination_examples()
    # filter_combination_examples()
    
    # For async examples:
    # asyncio.run(async_search_examples())
    
    print("\\nTo run these examples:")
    print("1. Replace the client credentials with your actual values")
    print("2. Uncomment the example functions you want to test")
    print("3. Run the script")
    print("\\nFor more information, see the README.md file.")
