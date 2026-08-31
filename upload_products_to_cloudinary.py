import os
import cloudinary
import cloudinary.uploader
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
django.setup()

from buy.models import Product


# Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

MEDIA_PRODUCTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "media",
    "products"
)

products = Product.objects.exclude(image="")

print(f"Found {products.count()} products with images.\n")

for product in products:
    image_name = os.path.basename(product.image.name)
    local_path = os.path.join(MEDIA_PRODUCTS, image_name)

    print(f"Product: {product.name}")
    print(f"Image:   {image_name}")

    if not os.path.exists(local_path):
        print("❌ Local image not found\n")
        continue

    try:
        result = cloudinary.uploader.upload(
            local_path,
            folder="products",
            resource_type="image",
        )

        public_id = result["public_id"]

        # Store the Cloudinary public ID in the ImageField
        product.image.name = public_id
        product.save(update_fields=["image"])

        print(f"✅ Uploaded: {public_id}\n")

    except Exception as e:
        print(f"❌ Upload failed: {e}\n")

print("Migration finished.")