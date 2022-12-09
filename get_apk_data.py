import os.path
import time

from androguard.core.bytecodes.apk import APK
from androguard.misc import AnalyzeAPK
import util
from util import logger


def get_features(file_path):
    time_start = time.time()
    if os.path.isdir(file_path):
        return
    file_output_parts = os.path.splitext(file_path)[0].split("/")
    file_output_parts[-1] += ".json"
    file_output_parts.insert(len(file_output_parts)-1, "json")
    file_output_path = ""
    for part in file_output_parts:
        file_output_path = os.path.join(file_output_path, part)
    file_output_dir = file_output_path[:file_output_path.rfind("\\")]
    if not os.path.exists(file_output_dir):
        os.mkdir(file_output_dir)
    if os.path.exists(file_output_path):
        logger.info("the APK " + file_path + " already abstracted")
        return

    logger.info("start to analyze the APK " + file_path + "...")
    a = APK(file_path)
    data = {}
    declared_xml_pms = set()
    declared_pms = set()
    activities = set()
    services = set()
    providers = set()
    receivers = set()
    hardware = set()

    for pms in a.get_permissions():
        declared_xml_pms.add(pms)
    for pms in a.get_declared_permissions():
        declared_pms.add(pms)
    for activity in a.get_activities():
        activities.add(activity)
    for service in a.get_services():
        services.add(service)
    for provider in a.get_providers():
        providers.add(provider)
    for receiver in a.get_receivers():
        receivers.add(receiver)
    for feature in a.get_features():
        hardware.add(feature)
    data['declared_xml_pms'] = declared_xml_pms
    data['declared_pms'] = declared_pms
    data['activities'] = activities
    data['services'] = services
    data['providers'] = providers
    data['receivers'] = receivers
    data['hardware'] = hardware

    sensitive_apis = set()
    android_suspicious_apis = ["getExternalStorageDirectory", "getSimCountryIso", "execHttpRequest",
                               "sendTextMessage", "getSubscriberId", "getDeviceId", "getPackageInfo",
                               "getSystemService", "getWifiState",
                               "setWifiEnabled", "setWifiDisabled", "Cipher"]
    other_suspicious_apis = ["Ljava/net/HttpURLconnection;->setRequestMethod(Ljava/lang/String;)",
                             "Ljava/net/HttpURLconnection",
                             "Lorg/apache/http/client/methods/HttpPost",
                             "Landroid/telephony/SmsMessage;->getMessageBody",
                             "Ljava/io/IOException;->printStackTrace", "Ljava/lang/Runtime;->exec"]
    a, d, dx = AnalyzeAPK(file_path)
    for method in dx.get_methods():
        api = str(method.get_method())
        for other_suspicious_api in other_suspicious_apis:
            if other_suspicious_api in api:
                sensitive_apis.add(api)
        if (";->" not in api) or (not api.startswith("Landroid")):
            continue
        api_parts = api.split(";->")
        api_class = api_parts[0].strip()
        api_name = api_parts[1].split("(")[0].strip()
        if api_name in android_suspicious_apis:
            sensitive_apis.add(api_class + ";->" + api_name)
    data['sensitive_apis'] = sensitive_apis

    util.get_json(file_output_path, data)
    time_final = time.time()
    logger.info(file_path + " analyzed successfully in " + str(time_final - time_start) + "s")


def solution(*paths):
    apk_list = []
    for path in paths:
        apk_list.extend(util.get_file_list(path))

    for path in apk_list:
        get_features(path)
