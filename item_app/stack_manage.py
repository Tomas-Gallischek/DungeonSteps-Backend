from profile_app.models import Player_Item_Material
from item_app.models import Item_default
from django.db.models import Sum

# V tuhle chvíli už utemy u hráče JSOU a jen chceme sloučit ty které tam jsou vícekrát, ostatní ignorujeme pomocí pass
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
        item_substance = all_items.filter(item_base_id=base_id).count()
        if item_substance > 1:
            print(f"Množství itemů s base ID {base_id} je {item_substance}, stackuji...")
            item = all_items.filter(item_base_id=base_id).aggregate(Sum('amount'))
            all_items.filter(item_base_id=base_id).delete()
            item_default = Item_default.objects.select_related('material_details').get(item_base_id=base_id)
            
            all_items.create(
                player=player,
                item_base_id=base_id,
                item_status='inventory',
                amount=item['amount__sum'],
                item_img_ozn = item_default.item_img_ozn,
                name=item_default.name,
                description=item_default.description,
                category=item_default.category,
                lvl_req=item_default.lvl_req,
                rarity=item_default.material_details.rarity,
                price_ks=item_default.material_details.price_ks,
                stack_able=True,
            )
            print(f"Nové množství itemu s base ID {base_id} je {item['amount__sum']}")
        else:
            print(f"Množství itemů s base ID {base_id} je {item_substance}, není potřeba stackovat.")
            pass