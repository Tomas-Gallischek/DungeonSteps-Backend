from profile_app.models import Player_Item_Material
from item_app.models import Item_default
from django.db.models import Sum

def stacks_items(player):
    print('stacking items')
    base_id_list = []
    all_items = Player_Item_Material.objects.filter(player=player, stack_able=True)
    for item in all_items:

        if item.item_base_id not in base_id_list:
            base_id_list.append(item.item_base_id)
        else:
            pass
        
    for base_id in base_id_list:
        item = all_items.filter(item_base_id=base_id).aggregate(Sum('amount'))
        all_items.filter(item_base_id=base_id).delete()
        item_default = Item_default.objects.select_related('material_details').get(item_base_id=base_id)
        price_all = item_default.material_details.price_ks * item['amount__sum']
        print(f"{item_default.name} - {item_default.material_details.rarity} - total amount: {item['amount__sum']}")
        
        all_items.create(
            player=player,
            item_base_id=base_id,
            item_status='inventory',
            amount=item['amount__sum'],
            name=item_default.name,
            description=item_default.description,
            category=item_default.category,
            lvl_req=item_default.lvl_req,
            rarity=item_default.material_details.rarity,
            price_ks=item_default.material_details.price_ks,
            price_all=price_all,
            stack_able=True,
        )
        print(f"stacked {item['amount__sum']} of {item_default.name}")