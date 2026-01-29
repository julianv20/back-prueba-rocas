"""Seed data for testing"""
import asyncio
from datetime import date, timedelta
import random

from app.infrastructure.driven_adapter.persistence.config.database import Database
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from app.infrastructure.driven_adapter.persistence.stock_repository.sqlalchemy_stock_repository import (
    SQLAlchemyStockRepository
)
from app.domain.model.user import User
from app.domain.model.stock import Product, Warehouse, StockMove, StockMoveType
from app.domain.usecase.util.security import SecurityService
from app.application.settings import settings

# Initialize database
db = Database(database_url=settings.database_url)
db.create_database()

# Initialize repositories
user_repo = SQLAlchemyUserRepository(session_factory=db.session)
stock_repo = SQLAlchemyStockRepository(session_factory=db.session)

# Security service
security = SecurityService()


async def seed_users():
    """Seed initial users"""
    print("🔐 Seeding users...")
    
    users = [
        User(
            id="1234567890",
            name="Admin",
            last_name="User",
            email="admin@example.com",
            password=security.hash_password("admin123")
        ),
        User(
            id="0987654321",
            name="Test",
            last_name="User",
            email="test@example.com",
            password=security.hash_password("test123")
        ),
        User(
            id="1122334455",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password=security.hash_password("john123")
        ),
        User(
            id="5544332211",
            name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password=security.hash_password("jane123")
        )
    ]
    
    created_count = 0
    for user in users:
        try:
            existing = await user_repo.find_by_email(user.email)
            if not existing:
                await user_repo.create(user)
                created_count += 1
        except Exception as e:
            print(f"   ❌ Error creating user {user.email}: {e}")
    
    print(f"   ✅ {created_count} users created")


async def seed_products():
    """Seed 150 products with different categories"""
    print("📦 Seeding products...")
    
    # Categories and product templates
    categories = {
        "Laptops": [
            "Dell XPS", "HP Pavilion", "Lenovo ThinkPad", "ASUS VivoBook", 
            "Acer Aspire", "MSI Prestige", "Razer Blade", "LG Gram",
            "Samsung Galaxy Book", "Microsoft Surface Laptop", "Huawei MateBook",
            "MacBook Air", "MacBook Pro", "Alienware", "ROG Zephyrus"
        ],
        "Smartphones": [
            "iPhone 15", "iPhone 14", "iPhone 13", "Samsung Galaxy S24",
            "Samsung Galaxy S23", "Samsung Galaxy A54", "Xiaomi 14",
            "Xiaomi 13", "Google Pixel 8", "Google Pixel 7",
            "OnePlus 12", "OnePlus 11", "OPPO Find X6", "Realme GT",
            "Motorola Edge", "Sony Xperia", "Nothing Phone", "Vivo X90"
        ],
        "Tablets": [
            "iPad Pro 12.9", "iPad Pro 11", "iPad Air", "iPad Mini",
            "Samsung Galaxy Tab S9", "Samsung Galaxy Tab A9", "Lenovo Tab P12",
            "Xiaomi Pad 6", "Huawei MatePad", "Amazon Fire HD", "Surface Pro"
        ],
        "Monitors": [
            "Dell UltraSharp", "LG UltraGear", "Samsung Odyssey", "ASUS ProArt",
            "BenQ PD", "AOC Gaming", "ViewSonic VP", "HP Z27",
            "Acer Predator", "MSI Optix", "Gigabyte M32U"
        ],
        "Keyboards": [
            "Logitech MX Keys", "Corsair K95", "Razer BlackWidow", "Keychron K8",
            "Anne Pro 2", "Ducky One 3", "HyperX Alloy", "SteelSeries Apex",
            "ASUS ROG Strix", "Cooler Master CK"
        ],
        "Mice": [
            "Logitech MX Master 3S", "Razer DeathAdder", "Corsair Dark Core",
            "SteelSeries Rival", "Glorious Model O", "Logitech G502",
            "Razer Viper", "BenQ Zowie EC", "Roccat Kone"
        ],
        "Headphones": [
            "Sony WH-1000XM5", "Bose QuietComfort", "Apple AirPods Max",
            "Sennheiser Momentum", "Jabra Elite", "Samsung Galaxy Buds",
            "Beats Studio", "Audio-Technica ATH", "HyperX Cloud"
        ],
        "Smartwatches": [
            "Apple Watch Series 9", "Samsung Galaxy Watch 6", "Garmin Fenix",
            "Fitbit Sense", "Amazfit GTR", "Huawei Watch GT", "TicWatch Pro"
        ],
        "Cameras": [
            "Canon EOS R6", "Sony A7 IV", "Nikon Z6 II", "Fujifilm X-T5",
            "Panasonic Lumix S5", "GoPro Hero 12", "DJI Osmo Action"
        ],
        "Storage": [
            "Samsung SSD 980 PRO", "WD Black SN850X", "Crucial P5 Plus",
            "Seagate Barracuda", "Kingston NV2", "Sandisk Extreme"
        ]
    }
    
    products = []
    product_id = 1
    
    for category, items in categories.items():
        for item in items:
            # Generate multiple variants per item
            variants = ["", " Plus", " Pro", " Ultra", " Max"]
            for variant in variants[:3]:  # 3 variants max per item
                if product_id > 150:
                    break
                
                full_name = f"{item}{variant}"
                sku = f"{category[:3].upper()}-{str(product_id).zfill(4)}"
                
                products.append(
                    Product(
                        id=f"P{str(product_id).zfill(3)}",
                        name=full_name,
                        sku=sku
                    )
                )
                product_id += 1
            
            if product_id > 150:
                break
        
        if product_id > 150:
            break
    
    created_count = 0
    for i, product in enumerate(products[:150], 1):
        try:
            existing = await stock_repo.find_product_by_id(product.id)
            if not existing:
                await stock_repo.create_product(product)
                created_count += 1
                
                # Show progress every 30 items
                if i % 30 == 0:
                    print(f"   📈 Progress: {i}/150 products created...")
        except Exception as e:
            print(f"   ❌ Error creating product {product.name}: {e}")
    
    print(f"   ✅ {created_count} products created")


async def seed_warehouses():
    """Seed initial warehouses"""
    print("🏭 Seeding warehouses...")
    
    warehouses = [
        Warehouse(id="W001", name="Bodega Central"),
        Warehouse(id="W002", name="Bodega Norte"),
        Warehouse(id="W003", name="Bodega Sur"),
        Warehouse(id="W004", name="Bodega Este"),
        Warehouse(id="W005", name="Bodega Oeste"),
        Warehouse(id="W006", name="Bodega Internacional"),
    ]
    
    created_count = 0
    for warehouse in warehouses:
        try:
            existing = await stock_repo.find_warehouse_by_id(warehouse.id)
            if not existing:
                await stock_repo.create_warehouse(warehouse)
                created_count += 1
        except Exception as e:
            print(f"   ❌ Error creating warehouse {warehouse.name}: {e}")
    
    print(f"   ✅ {created_count} warehouses created")


async def seed_stock_moves():
    """Seed 30 stock moves with realistic data"""
    print("📊 Seeding stock moves...")
    
    # Get products and warehouses
    products = await stock_repo.find_all_products()
    warehouses = await stock_repo.find_all_warehouses()
    
    if not products or not warehouses:
        print("   ❌ No products or warehouses found. Seed them first.")
        return
    
    # Reference templates
    in_references = [
        "Compra a proveedor principal",
        "Restock mensual programado",
        "Importación directa desde fábrica",
        "Compra por demanda alta",
        "Stock de seguridad Q1",
        "Pedido especial corporativo",
        "Reposición automática",
        "Compra al por mayor",
        "Importación urgente",
        "Pedido regular trimestral"
    ]
    
    out_references = [
        "Venta online - Cliente premium",
        "Venta en tienda física",
        "Pedido corporativo - Empresa XYZ",
        "Distribución a sucursales",
        "Venta mayorista B2B",
        "Cliente VIP - Pedido especial",
        "Pedido express mismo día",
        "Venta campaña promocional",
        "Pre-orden cumplida",
        "Venta Black Friday"
    ]
    
    adjust_references = [
        "Ajuste por inventario físico mensual",
        "Corrección de stock por auditoría",
        "Producto dañado en tránsito",
        "Devolución proveedor - Defecto",
        "Ajuste por diferencia sistema",
        "Corrección error registro",
        "Merma detectada en bodega",
        "Reconciliación fin de mes",
        "Ajuste contable trimestral"
    ]
    
    start_date = date(2025, 1, 1)
    created_count = 0
    
    # Generate 30 stock moves
    for i in range(30):
        move_id = f"SM{str(i+1).zfill(3)}"
        
        # Random date in the last 6 months
        random_days = random.randint(0, 180)
        move_date = start_date + timedelta(days=random_days)
        
        # Random product and warehouse
        product = random.choice(products)
        warehouse = random.choice(warehouses)
        
        # Random type with weighted probability
        type_weights = [0.5, 0.35, 0.15]  # IN, OUT, ADJUST
        move_type = random.choices(
            [StockMoveType.IN, StockMoveType.OUT, StockMoveType.ADJUST],
            weights=type_weights
        )[0]
        
        # Quantity and reference based on type
        if move_type == StockMoveType.IN:
            quantity = random.randint(20, 150)
            reference = random.choice(in_references)
        elif move_type == StockMoveType.OUT:
            quantity = random.randint(5, 80)
            reference = random.choice(out_references)
        else:  # ADJUST
            quantity = random.randint(1, 30)
            reference = random.choice(adjust_references)
        
        stock_move = StockMove(
            id=move_id,
            date=move_date,
            product=product,
            warehouse=warehouse,
            type=move_type,
            quantity=quantity,
            reference=reference
        )
        
        try:
            existing = await stock_repo.find_stock_move_by_id(stock_move.id)
            if not existing:
                await stock_repo.create_stock_move(stock_move)
                created_count += 1
                
                # Show progress every 10 items
                if (i + 1) % 10 == 0:
                    print(f"   📈 Progress: {i + 1}/30 stock moves created...")
        except Exception as e:
            print(f"   ❌ Error creating stock move {stock_move.id}: {e}")
    
    print(f"   ✅ {created_count} stock moves created")


async def main():
    """Main seed function"""
    print("\n" + "=" * 60)
    print("🌱 INICIANDO SEED DE LA BASE DE DATOS")
    print("=" * 60 + "\n")
    
    await seed_users()
    print()
    
    await seed_products()
    print()
    
    await seed_warehouses()
    print()
    
    await seed_stock_moves()
    
    print("\n" + "=" * 60)
    print("🎉 SEED COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print("\n📊 RESUMEN:")
    print("   • 4 usuarios creados")
    print("   • 150 productos creados")
    print("   • 6 bodegas creadas")
    print("   • 30 movimientos de stock creados")
    print("\n👤 USUARIOS DE PRUEBA:")
    print("   • admin@example.com / admin123")
    print("   • test@example.com / test123")
    print("   • john.doe@example.com / john123")
    print("   • jane.smith@example.com / jane123")
    print("\n🚀 SERVIDOR:")
    print("   python -m uvicorn app.main:app --reload")
    print("\n📚 DOCUMENTACIÓN:")
    print("   http://localhost:8000/api/docs")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())