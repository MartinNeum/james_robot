import logging, json
from telegram import Update
from telegram.ext import ContextTypes

SHOPPING_LIST = 'shoppinglist.json'

async def add_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /add*"
    syntax_text = "Please use this format: /add `item1` `item2`"
    format_text = "• For `item` paste the item you want to add. You can paste multiple items by seperating them with a space."
    example_text = "`/add Apples Cheese`\n\nIn this example, James will add 'Apples' and 'Cheese' to your shopping list."
    
    try:
        items_to_add = context.args

        if len(items_to_add) < 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return
        
        try:
            with open(SHOPPING_LIST, 'r') as file:
                shoppinglists = json.load(file)
        except FileNotFoundError:
            shoppinglists = []

        # Finde shoppinglist
        list_exists = False
        for list in shoppinglists:
            if list['chat_id'] == update.effective_chat.id:
                list_exists = True
                for item in items_to_add:
                    list['items'].append(item)

        # Erstelle List wenn nicht vorhanden
        if not list_exists:
            new_shoppinglist = {
                "chat_id": update.effective_chat.id,
                "items": items_to_add
            }

            shoppinglists.append(new_shoppinglist)

        with open(SHOPPING_LIST, 'w') as file:
            json.dump(shoppinglists, file, indent=2)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Item(s) added.", parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def remove_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /remove*"
    syntax_text = "Please use this format: /remove `item1` `item2`"
    format_text = "• For `item` paste the item you want to remove. You can paste multiple items by seperating them with a space."
    example_text = "`/remove Apples Cheese`\n\nIn this example, James will remove 'Apples' and 'Cheese' from your shopping list."

    try:
        items_to_remove = context.args

        if len(items_to_remove) < 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return
        
        try:
            with open(SHOPPING_LIST, 'r') as file:
                shoppinglists = json.load(file)
        except FileNotFoundError:
            shoppinglists = []

        # Finde shoppinglist
        list_exists = False
        items_not_found = []
        for list in shoppinglists:
            if list['chat_id'] == update.effective_chat.id:
                list_exists = True
                for item in items_to_remove:
                    if item in list['items']:
                        list['items'].remove(item)
                    else:
                        items_not_found.append(item)

        # Liste existiert nicht
        if not list_exists:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="🤔 It seems you don't have a list yet. You can create one by using /add. 😊")
            return

        with open(SHOPPING_LIST, 'w') as file:
            json.dump(shoppinglists, file, indent=2)

        if not len(items_not_found) == len(items_to_remove):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Item(s) removed.", parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Uuups! 🤔 I couldn't find the item(s). Please check for typos and try again.", parse_mode='Markdown')

        # Liste Items die nicht gefunden wurden
        if len(items_not_found) > 0:
            not_found_string = ", ".join(items_not_found)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"_{not_found_string} couldn't be found._", parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def get_shoppinglist(update: Update, context: ContextTypes.DEFAULT_TYPE):

    items_string = f"📃 *{update.effective_user.first_name}'s Shoppinglist*\n\n"

    try:
        with open(SHOPPING_LIST, 'r') as file:
            shoppinglists = json.load(file)
        
        # Finde shoppinglist
        list_exists = False
        for list in shoppinglists:
            if list['chat_id'] == update.effective_chat.id:
                list_exists = True
                if len(list['items']) == 0:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"💁‍♂️ Your list is empty - let's make some wishes! 💭🧞‍♀️", parse_mode='Markdown')
                    return
                for item in list['items']:
                    items_string += f"• {item}\n"

        if not list_exists:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="🤔 It seems you don't have a list yet. You can create one by using /add. 😊")
            return
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=items_string, parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def clear_shoppinglist(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        with open(SHOPPING_LIST, 'r') as file:
            shoppinglists = json.load(file)
        
        # Finde shoppinglist
        list_exists = False
        for list in shoppinglists:
            if list['chat_id'] == update.effective_chat.id:
                list_exists = True
                list['items'].clear()
            
            with open(SHOPPING_LIST, 'w') as file:
                json.dump(shoppinglists, file, indent=2)

        if not list_exists:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="🤔 It seems you don't have a list yet. You can create one by using /add. 😊")
            return
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Shoppinglist is clear.", parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")
    