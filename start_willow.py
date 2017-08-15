#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from ProfWillow.utils import get_args, get_dicts
from ProfWillow.clients import start_clients

logging.basicConfig(format='[%(name)10.10s][%(levelname)8.8s] %(message)s',
                    level=logging.INFO)
log = logging.getLogger('server')
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)

args = get_args()


def start_bots():
    log.info("{} bot(s) to be started".format(len(args.tokens)))
    if len(args.feed_channels) > 1:
        log.info("{} feed channels set".format(len(args.feed_channels)))
    else:
        log.info("Feed channel set to {}".format(args.feed_channels[0]))
    if args.subscription_channel is not None:
        log.info("Subscription channel set to {}".format(
            args.subscription_channel))
    else:
        log.info("No subscription channel set")
    if args.test_channel is not None:
        log.info("Test channel set to {}".format(args.test_channel))
    else:
        log.info("No test channel set")
    if args.areas is not None:
        log.info("{} area/geofences set".format(len(args.areas)))
    if args.muted_role is not None:
        log.info("Muted role set to {}".format(args.muted_role))
    else:
        log.info("No muted role set")
    if args.all_areas is True:
        log.info("All users will automatically be added to all areas")
    else:
        log.info("All users will automatically be added to no areas")
    log.info("Setting up dictionaries")
    dicts = get_dicts(len(args.tokens))
    log.info("Starting Clients")
    start_clients()

###############################################################################


if __name__ == '__main__':
    log.info("ProfessowWillow is getting ready...")
    start_bots()
