# examples/magic_search_examples.py

"""
Magic Search Examples for Myer PIM SDK

This file demonstrates the enhanced "magic" search functionality that makes it
easy to search by any product value in the Akeneo PIM system.
"""

import asyncio
from myer_pim_sdk import AkeneoClient, AkeneoAsyncClient, SearchBuilder
from myer_pim_sdk.search import (
    by_supplier_style, by_brand, ready_for_enrichment, 
    enrichment_complete, missing_images, by_supplier,
    concession_products, online_products, clearance_products
)


def basic_magic_search_examples():
    """Examples of the new magic search functionality."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("=== Magic Search Examples ===")
    
    # 1. Generic attribute search - the "magic" method
    print("\\n1. Generic attribute search...")
    products = client.product_models.search_with_builder(
        lambda f: f.by_attribute("supplier_style", "FI02847")
                  .by_attribute("copy_status", "20")
                  .by_attribute("concession", True)
    )
    print(f"Found {len(products)} products with supplier style FI02847, copy status 20, and concession=true")
    
    # 2. Myer-specific convenience methods
    print("\\n2. Myer-specific convenience methods...")
    country_road_products = client.product_models.search_with_builder(
        lambda f: f.brand("Country Road")
                  .online_category("women_accessories")
                  .online_ind(True)
    )
    print(f"Found {len(country_road_products)} Country Road products in women's accessories that are online")
    
    # 3. Enrichment status searches
    print("\\n3. Enrichment status searches...")
    ready_for_images = client.product_models.search_with_builder(
        lambda f: f.image_status("10")  # Status 10 = ready
                  .myer_image_status("10")
    )
    print(f"Found {len(ready_for_images)} product models ready for image enrichment")
    
    # 4. Complex Myer workflows
    print("\\n4. Complex Myer workflows...")
    enrichment_candidates = client.product_models.search_with_builder(
        lambda f: f.copy_status("20")  # Copy complete
                  .image_status("10")  # Ready for images
                  .supplier_trust_level(["gold", "silver"])  # High trust suppliers
                  .online_ind(True)  # Available online
    )
    print(f"Found {len(enrichment_candidates)} models with copy complete, ready for images, from trusted suppliers")


def value_filtering_examples():
    """Examples of filtering returned product values."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Value Filtering Examples ===")
    
    # 1. Filter to only return specific attributes
    print("\\n1. Only return specific attributes...")
    builder = (SearchBuilder()
               .filters(lambda f: f.brand("Country Road"))
               .attributes(["supplier_style", "online_name", "brand", "copy_status"])
               .limit(5))
    
    products = client.product_models.search_with_builder(builder)
    print(f"Found {len(products)} Country Road products with only specific attributes returned")
    if products:
        print(f"First product attributes: {list(products[0].values.keys())}")
    
    # 2. Filter by locale
    print("\\n2. Filter by locale...")
    builder = (SearchBuilder()
               .filters(lambda f: f.online_category("women_accessories"))
               .locales(["en_AU"])
               .attributes(["online_name", "brand", "online_long_desc"])
               .limit(3))
    
    products = client.product_models.search_with_builder(builder)
    print(f"Found {len(products)} women's accessories with only en_AU locale values")
    
    # 3. Filter by scope/channel
    print("\\n3. Filter by scope/channel...")
    builder = (SearchBuilder()
               .filters(lambda f: f.buyable_ind(True))
               .scope("ecommerce")
               .attributes(["online_name", "brand", "online_long_desc"])
               .limit(3))
    
    products = client.product_models.search_with_builder(builder)
    print(f"Found {len(products)} buyable products with only ecommerce scope values")


def quick_search_functions_examples():
    """Examples using the quick search functions."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Quick Search Functions ===")
    
    # 1. Search by supplier style
    print("\\n1. Search by supplier style...")
    products = client.product_models.search_with_builder(by_supplier_style("FI02847"))
    print(f"Found {len(products)} products with supplier style FI02847")
    
    # 2. Search by brand
    print("\\n2. Search by brand...")
    products = client.product_models.search_with_builder(by_brand("Cue"))
    print(f"Found {len(products)} Cue products")
    
    # 3. Find products ready for enrichment
    print("\\n3. Find products ready for enrichment...")
    products = client.product_models.search_with_builder(ready_for_enrichment("image", 10))
    print(f"Found {len(products)} products ready for image enrichment")
    
    # 4. Find products with enrichment complete
    print("\\n4. Find products with enrichment complete...")
    products = client.product_models.search_with_builder(enrichment_complete("copy", 20))
    print(f"Found {len(products)} products with copy enrichment complete")
    
    # 5. Find products missing images
    print("\\n5. Find products missing images...")
    products = client.product_models.search_with_builder(missing_images(1))
    print(f"Found {len(products)} products missing image 1")
    
    # 6. Search by supplier
    print("\\n6. Search by supplier...")
    products = client.product_models.search_with_builder(by_supplier("9000395"))
    print(f"Found {len(products)} products from supplier 9000395")
    
    # 7. Find concession products
    print("\\n7. Find concession products...")
    products = client.product_models.search_with_builder(concession_products(True))
    print(f"Found {len(products)} concession products")
    
    # 8. Find online products
    print("\\n8. Find online products...")
    products = client.product_models.search_with_builder(online_products())
    print(f"Found {len(products)} online buyable products")
    
    # 9. Find clearance products
    print("\\n9. Find clearance products...")
    products = client.product_models.search_with_builder(clearance_products())
    print(f"Found {len(products)} clearance products")


def complex_enrichment_workflows():
    """Complex real-world enrichment workflow examples."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Complex Enrichment Workflows ===")
    
    # 1. Products needing both copy and image enrichment
    print("\\n1. Products needing comprehensive enrichment...")
    products = client.product_models.search_with_builder(
        lambda f: f.copy_status("10")  # Copy ready
                  .image_status("10")  # Image ready
                  .missing_description()  # No description yet
                  .missing_images(1)  # No images yet
                  .supplier_trust_level(["gold", "silver"])  # Trusted suppliers only
    )
    print(f"Found {len(products)} products needing both copy and image enrichment")
    
    # 2. Witchery products in women's accessories needing images
    print("\\n2. Witchery women's accessories needing images...")
    products = client.product_models.search_with_builder(
        lambda f: f.brand("Witchery")
                  .online_department("women")
                  .online_category("women_accessories")
                  .copy_status("20")  # Copy complete
                  .image_status("10")  # Ready for images
                  .has_description()  # Has description
                  .missing_images(1)  # Missing images
    )
    print(f"Found {len(products)} Witchery women's accessories needing images")
    
    # 3. High-priority enrichment queue
    print("\\n3. High-priority enrichment queue...")
    products = client.product_models.search_with_builder(
        lambda f: f.online_ind(True)  # Available online
                  .buyable_ind(True)  # Buyable
                  .concession(False)  # Not concession (direct Myer)
                  .clearance_ind(False)  # Not clearance
                  .copy_status("10")  # Ready for copy
                  .supplier_trust_level(["gold"])  # Gold suppliers only
    )
    print(f"Found {len(products)} high-priority products for enrichment")
    
    # 4. Audit incomplete enrichment
    print("\\n4. Audit incomplete enrichment...")
    products = client.product_models.search_with_builder(
        lambda f: f.copy_status("20")  # Copy supposedly complete
                  .myer_copy_status("10")  # But Myer status disagrees
                  .online_ind(True)
    )
    print(f"Found {len(products)} products with enrichment status discrepancies")
    
    # 5. Products ready for final review
    print("\\n5. Products ready for final review...")
    products = client.product_models.search_with_builder(
        lambda f: f.copy_status("20")  # Copy complete
                  .image_status("20")  # Images complete
                  .myer_copy_status("20")  # Myer copy complete
                  .myer_image_status("20")  # Myer images complete
                  .has_description()  # Has description
                  .has_images(1)  # Has at least image 1
    )
    print(f"Found {len(products)} products ready for final review")


def supplier_analysis_examples():
    """Examples for supplier analysis and management."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Supplier Analysis Examples ===")
    
    # 1. Analyze supplier performance by trust level
    trust_levels = ["gold", "silver", "bronze"]
    for level in trust_levels:
        products = client.product_models.search_with_builder(
            lambda f: f.supplier_trust_level([level])
                      .copy_status("20")
                      .image_status("20")
        )
        print(f"\\n{level.title()} suppliers: {len(products)} products fully enriched")
    
    # 2. Find suppliers with enrichment backlogs
    print("\\n2. Suppliers with enrichment backlogs...")
    suppliers_with_backlogs = {}
    
    # Get all products ready for enrichment
    backlog_products = client.product_models.search_with_builder(
        lambda f: f.copy_status("10")  # Ready but not complete
                  .online_ind(True)
    )
    
    print(f"Found {len(backlog_products)} products in copy enrichment backlog")
    
    # 3. Concession vs Direct Myer analysis
    print("\\n3. Concession vs Direct Myer analysis...")
    concession_ready = client.product_models.search_with_builder(
        lambda f: f.concession(True)
                  .copy_status("10")
                  .image_status("10")
    )
    
    direct_ready = client.product_models.search_with_builder(
        lambda f: f.concession(False)
                  .copy_status("10")
                  .image_status("10")
    )
    
    print(f"Concession products ready for enrichment: {len(concession_ready)}")
    print(f"Direct Myer products ready for enrichment: {len(direct_ready)}")


async def async_magic_search_examples():
    """Asynchronous examples of magic search."""
    
    client = AkeneoAsyncClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    try:
        print("\\n=== Async Magic Search Examples ===")
        
        # 1. Parallel enrichment status checks
        print("\\n1. Parallel enrichment status checks...")
        results = await asyncio.gather(
            client.product_models.search_with_builder_async(
                lambda f: f.copy_status("10")
            ),
            client.product_models.search_with_builder_async(
                lambda f: f.image_status("10")
            ),
            client.product_models.search_with_builder_async(
                lambda f: f.copy_status("20").image_status("20")
            )
        )
        
        copy_ready, image_ready, fully_complete = results
        print(f"Copy ready: {len(copy_ready)} products")
        print(f"Image ready: {len(image_ready)} products")
        print(f"Fully complete: {len(fully_complete)} products")
        
        # 2. Async supplier analysis
        print("\\n2. Async supplier analysis...")
        oxford_products = await client.product_models.search_with_builder_async(
            lambda f: f.brand("Oxford")
                      .supplier_trust_level(["gold", "silver"])
                      .online_ind(True)
        )
        print(f"Found {len(oxford_products)} Oxford products from trusted suppliers")
        
    finally:
        await client.close()


def practical_usage_examples():
    """Practical usage examples for daily Myer operations."""
    
    client = AkeneoClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        base_url="https://your-pim.akeneo.com"
    )
    
    print("\\n=== Practical Usage Examples ===")
    
    # 1. Daily enrichment dashboard
    print("\\n1. Daily enrichment dashboard...")
    
    # Get only the data we need for the dashboard
    dashboard_builder = (SearchBuilder()
                        .attributes(["supplier_style", "brand", "copy_status", "image_status", 
                                   "myer_copy_status", "myer_image_status", "online_name"])
                        .locales(["en_AU"])
                        .scope("ecommerce")
                        .limit(100))
    
    # Copy queue
    copy_queue = client.product_models.search_with_builder(
        dashboard_builder.filters(lambda f: f.copy_status("10"))
    )
    
    # Image queue  
    image_queue = client.product_models.search_with_builder(
        dashboard_builder.filters(lambda f: f.image_status("10"))
    )
    
    print(f"Copy queue: {len(copy_queue)} products")
    print(f"Image queue: {len(image_queue)} products")
    
    # 2. Find specific product by supplier style (common lookup)
    print("\\n2. Find specific product by supplier style...")
    product = client.product_models.search_with_builder(
        lambda f: f.supplier_style("FI02847")
    )
    if product:
        p = product[0]
        print(f"Found: {p.values.get('online_name', [{}])[0].data if p.values.get('online_name') else 'No name'}")
        print(f"Brand: {p.values.get('brand', [{}])[0].data if p.values.get('brand') else 'No brand'}")
        print(f"Copy Status: {p.values.get('copy_status', [{}])[0].data if p.values.get('copy_status') else 'Unknown'}")
    
    # 3. Bulk status check for specific supplier styles
    print("\\n3. Bulk status check for supplier styles...")
    supplier_styles = ["FI02847", "ABC123", "XYZ789"]  # Example styles
    
    products = client.product_models.search_with_builder(
        lambda f: f.supplier_style(supplier_styles)
                  .attributes(["supplier_style", "copy_status", "image_status"])
    )
    
    for product in products:
        style = product.values.get('supplier_style', [{}])[0].data if product.values.get('supplier_style') else 'Unknown'
        copy_status = product.values.get('copy_status', [{}])[0].data if product.values.get('copy_status') else 'Unknown'
        image_status = product.values.get('image_status', [{}])[0].data if product.values.get('image_status') else 'Unknown'
        print(f"  {style}: Copy={copy_status}, Image={image_status}")


if __name__ == "__main__":
    """
    Run magic search examples. In practice, you would run these individually
    and replace the client credentials with your actual values.
    """
    
    print("Myer PIM SDK - Magic Search Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run:
    
    # basic_magic_search_examples()
    # value_filtering_examples()
    # quick_search_functions_examples()
    # complex_enrichment_workflows()
    # supplier_analysis_examples()
    # practical_usage_examples()
    
    # For async examples:
    # asyncio.run(async_magic_search_examples())
    
    print("\\nTo run these examples:")
    print("1. Replace the client credentials with your actual values")
    print("2. Uncomment the example functions you want to test")
    print("3. Run the script")
    print("\\nMagic Search Features:")
    print("- Generic by_attribute() method for any product value")
    print("- Myer-specific convenience methods (supplier_style, brand, etc.)")
    print("- Value filtering (attributes, locales, scope)")
    print("- Quick search functions for common patterns")
    print("- Complex enrichment workflow support")
