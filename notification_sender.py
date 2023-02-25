from discord import SyncWebhook


def webhook2(output):
    empty_dict={}
    webhook_url = "https://discord.com/api/webhooks/1013398610156724315/lUJmmD7MzlbK35wMiNd0eFXFRXYuI-RPqT6egGsuR6NyfNBAmSv8OyeJ80U_fD-MtONw"
    webhook = SyncWebhook.from_url(webhook_url)
    if output == empty_dict:
        pass
    else:
        webhook.send(output)





if __name__ == "__main__":
    webhook2()
