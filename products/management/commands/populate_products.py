from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Poblar base de datos con productos de ejemplo'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Laptop HP 15',
                'description': 'Laptop HP 15" con procesador Intel Core i5, 8GB RAM, 256GB SSD',
                'price': 699.99,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'
            },
            {
                'name': 'Mouse Logitech MX Master 3',
                'description': 'Mouse inalámbrico ergonómico con precisión de seguimiento avanzada',
                'price': 99.99,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400'
            },
            {
                'name': 'Teclado Mecánico RGB',
                'description': 'Teclado mecánico con switches azules y retroiluminación RGB',
                'price': 129.99,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400'
            },
            {
                'name': 'Monitor Samsung 27"',
                'description': 'Monitor 27" Full HD con tecnología IPS y 75Hz',
                'price': 249.99,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400'
            },
            {
                'name': 'Webcam HD 1080p',
                'description': 'Cámara web con resolución Full HD y micrófono incorporado',
                'price': 59.99,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1526598319457-f040c10e2c00?w=400'
            },
            {
                'name': 'Auriculares Sony WH-1000XM4',
                'description': 'Auriculares inalámbricos con cancelación de ruido líder en la industria',
                'price': 349.99,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400'
            },
            {
                'name': 'SSD Samsung 1TB',
                'description': 'Unidad de estado sólido NVMe de 1TB con velocidades de hasta 3500 MB/s',
                'price': 119.99,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400'
            },
            {
                'name': 'Router WiFi 6 TP-Link',
                'description': 'Router de doble banda con tecnología WiFi 6 y cobertura de hasta 200m²',
                'price': 89.99,
                'stock': 45,
                'image_url': 'https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=400'
            },
            {
                'name': 'Hub USB-C 7 en 1',
                'description': 'Adaptador multipuerto con HDMI, USB 3.0, lector SD y carga rápida',
                'price': 39.99,
                'stock': 60,
                'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400'
            },
            {
                'name': 'Mochila Laptop 17"',
                'description': 'Mochila resistente al agua con compartimento acolchado para laptop',
                'price': 49.99,
                'stock': 55,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'
            },
        ]

        created_count = 0
        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Producto creado: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Producto ya existe: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado: {created_count} productos nuevos creados')
        )