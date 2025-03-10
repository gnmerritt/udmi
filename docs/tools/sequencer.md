[**UDMI**](../../) / [**Docs**](../) / [**Tools**](./) / [Sequencer](#)

# Sequencer Setup

The UDMI _sequencer_ tool monitors a sequence of messages from a device's stream and
validates that the composition of sequential messsages is compliant with the UDMI Schema

1.  Ensure you have [deployed the necessary cloud functions](../cloud/gcp/udmis.md) to your GCP project
2.  Add a new GCP IoT Core registry with a registry ID of `UDMS-REFLECT`.
    *   Use `udmi_reflect` as the default PUB/SUB topic for this registry.
    *   This serves as a _reflector_ of the MAIN IoT registry combining all messages
        published into a single stream.
3.  Create credentials for a reflector 'device' (there is no actual, physical device):
    *   On your local machine, run `mkdir validator` in the indended _site_model_ directory.
    *   Run `bin/keygen RS256 validator` to create a public and private key.
3.  Add a new device to the `UDMS-REFLECT` registry with the followong configuration:
    *   device_id: Use the `<Registry ID>` as defined in Site Model for the devices to be tested.
    *   auth_key: Use the public key you just created from `validator/rsa_public.pem`

## Running Sequencer

To run the _sequencer_, run the command from the top-level of the _site_model_ directory, with
an optional device serial number:
```
~/udmi/bin/sequence ${GCP_PROJECT_NAME} ${TARGET_DEVICE} ${SERIAL_NUMBER}
```

It's a good idea to make sure everything is setup properly by initially running the sequences
against the [pubber reference](pubber.md). Specifically note the _troubleshooting_ section.

## Troubleshooting

To increase the logging verbosity add a `-v` at the beginning of the command options, or add
another `-v` or just `-vv` to add even more details.

Adding a specific test names (e.g. `broken_config`) to the end will trigger just those explicitly
specified tests:

```
username@hostname:~/udmi$ bin/sequencer -vv udmi_site_model bos-udmi-proto AHU-1 broken_config
```

The sequence test that's being tested will be included along with many log messages, e.g.:
```
$ fgrep broken_config -r sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/ | head
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/config_system_2022-08-12T20:33:57.073Z.json:    "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/local_system_2022-08-12T20:34:10Z.json:    "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/config_update_2022-08-12T20:34:12.419Z.json:      "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/local_config_2022-08-12T20:33:57Z.json:      "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/local_system_2022-08-12T20:33:52Z.json:    "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/config_system_2022-08-12T20:33:55.191Z.json:    "sequence_name" : "broken_config"
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/system.log:2022-08-12T20:33:54Z DEBUG pubber State update (broken_config)
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/system.log:2022-08-12T20:33:56Z DEBUG pubber State update (broken_config)
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/system.log:2022-08-12T20:33:59Z DEBUG pubber State update (broken_config)
sites/udmi_site_model/out/devices/AHU-1/tests/broken_config/config_system_2022-08-12T20:34:12.396Z.json:    "sequence_name" : "broken_config"
```

## Example Output

An example output (using the pubber device), looks something like:

```
username@hostname:~/sites/bos-udmi-proto$ ~/udmi/bin/sequence bos-udmi-proto FAUX-01
Using pubber with serial sequencer-29581
Writing config to /tmp/validator_config.json:
{
  "project_id": "bos-udmi-proto",
  "site_model": "/home/username/sites/bos-udmi-proto",
  "device_id": "FAUX-01",
  "serial_no": "sequencer-29581",
  "key_file": "/home/username/sites/bos-udmi-proto/validator/rsa_private.pkcs8"
}
Writing pubber output to pubber.out
bin/pubber /home/username/sites/bos-udmi-proto bos-udmi-proto FAUX-01 sequencer-29581
Waiting for pubber startup 1...
Waiting for pubber startup 2...
Waiting for pubber startup 3...
Waiting for pubber startup 4...
INFO daq.pubber.Pubber - Connection complete.
Parsing /tmp/validator_config.json:
{
  "project_id": "bos-udmi-proto",
  "site_model": "/home/username/sites/bos-udmi-proto",
  "device_id": "FAUX-01",
  "serial_no": "sequencer-29581",
  "key_file": "/home/username/sites/bos-udmi-proto/validator/rsa_private.pkcs8"
}
Target project bos-udmi-proto
Site model /home/username/sites/bos-udmi-proto
Target device FAUX-01
Device serial sequencer-29581

> Task :compileJava
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: Some input files use unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.

Deprecated Gradle features were used in this build, making it incompatible with Gradle 7.0.
Use '--warning-mode all' to show the individual deprecation warnings.
See https://docs.gradle.org/6.8.2/userguide/command_line_interface.html#sec:command_line_warnings

BUILD SUCCESSFUL in 4s
2 actionable tasks: 2 executed
-rw-r--r-- 1 username primarygroup 34284160 May 24 22:14 build/libs/validator-1.0-SNAPSHOT-all.jar
Done with validator build.
java -cp validator/build/libs/validator-1.0-SNAPSHOT-all.jar org.junit.runner.JUnitCore com.google.daq.mqtt.validator.validations.WritebackValidator
JUnit version 4.13.1
Writing results to /home/username/udmi/out/devices/FAUX-01/RESULT.log
Validating device FAUX-01 serial sequencer-29581
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev token expiration sec 3600
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev creating client projects/bos-udmi-proto/locations/us-central1/registries/UDMS-REFLECT/devices/proto-dev on ssl://mqtt.googleapis.com:8883
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev creating new jwt
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev connecting to mqtt server
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev adding subscriptions
[main] INFO com.google.bos.iot.core.proxy.MqttPublisher - proto-dev done with setup connection
.2021-05-25T05:14:40Z starting test pointset_etag
2021-05-25T05:14:40Z sending system_config
2021-05-25T05:14:40Z sending pointset_config
2021-05-25T05:14:40Z sending system_config
2021-05-25T05:14:40Z updated system loglevel 400
2021-05-25T05:14:40Z sending pointset_config
2021-05-25T05:14:40Z updated pointset config_etag 1621919680268
2021-05-25T05:14:40Z waiting for etag 1621919680268
```
