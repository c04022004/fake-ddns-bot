# README.md

- Get yout token here: https://core.telegram.org/bots#3-how-do-i-create-a-bot
- Try a "wet-run" with `LIST_OF_ADMINS` assigned to be empty list, and interact with the bot on your telegram account. Check the log to find out your `chat_id` then add it back to your docker env.
- Remarks: `podman` is cool, but of couse, dokcer is also `okay`

```bash
# build the container image
cd ./fake-ddns-bot
podman build . -t fake-ddns-bot
podman run --detach --name fake-ddns-bot --env TELEGRAM_TOKEN="<YOUR-TOKEN-HERE>" \
--env LIST_OF_ADMINS="[<int>]" fake-ddns-bot
podman logs -f fake-ddns-bot
```

```bash
# config container to start on boot
# - check rootless pod systemd (https://access.redhat.com/discussions/5733161)
# - for docker, try '--restart unless-stopped'
podman generate systemd --name fake-ddns-bot > ~/.config/systemd/user/fake-ddns-bot.service
systemctl --user daemon-reload
systemctl --user enable fake-ddns-bot.service 
systemctl --user status fake-ddns-bot.service
```

---

This is some low effort work to salvage my [old project](https://github.com/c04022004/gprs-telegram-bot) to monitor my home internet uplink. Have a `Fedora Server` running `podman` 24/7 so it's good to know its IP for remote access.


