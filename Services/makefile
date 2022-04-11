SERVICES = read_serial docker_backend teststandAPI
START = $(addprefix start_,$(SERVICES))
LOGS = $(addprefix logs_,$(SERVICES))
STATUS = $(addprefix status_,$(SERVICES))
STOP = $(addprefix stop_,$(SERVICES))
CLEAN = $(addprefix clean_,$(SERVICES))

define start_service
	$(eval svc=$(subst start_,,$(1)))
	sudo systemctl stop $(svc).service
	sudo cp $(svc)/$(svc).service /etc/systemd/system/
	sudo systemctl start $(svc).service
endef

define status
	$(eval svc=$(subst status_,,$(1)))
	sudo systemctl status $(svc).service
endef

define clean
	$(eval svc=$(subst clean_,,$(1)))
	sudo rm $(svc)/*.csv
endef

define stop
	$(eval svc=$(subst stop_,,$(1)))
	sudo systemctl stop $(svc).service
endef

define watchlogs
	$(eval svc=$(subst logs_,,$(1)))
	journalctl -u $(svc) -f
endef

$(LOGS):
	$(call watchlogs,$(@))

$(STATUS):
	$(call status,$(@))

$(CLEAN):
	$(call clean,$(@))

$(START):
	$(call start_service,$(@))

$(STOP):
	$(call stop,$(@))