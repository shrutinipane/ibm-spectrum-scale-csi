import copy
import logging
import pytest
import ibm_spectrum_scale_csi.spectrum_scale_apis.fileset_functions as ff
import ibm_spectrum_scale_csi.scale_operator as scaleop
LOGGER = logging.getLogger()
pytestmark = [pytest.mark.volumesnapshot, pytest.mark.remotecluster]

@pytest.fixture(scope='session', autouse=True)
def values(request, check_csi_operator):
    global data, remote_data, snapshot_object, kubeconfig_value  # are required in every testcase
    kubeconfig_value, clusterconfig_value, operator_namespace, test_namespace, runslow_val, operator_yaml = scaleop.get_cmd_values(request)

    data = scaleop.read_driver_data(clusterconfig_value, test_namespace, operator_namespace, kubeconfig_value)
    keep_objects = data["keepobjects"]
    if not("remote" in data):
        LOGGER.error("remote data is not provided in cr file")
        assert False

    remote_data = scaleop.get_remote_data(data)
    ff.cred_check(remote_data)
    ff.set_data(remote_data)

    if runslow_val:
        value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi"},
                     {"access_modes": "ReadWriteOnce", "storage": "1Gi"}]
    else:
        value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi"}]
    value_vs_class = {"deletionPolicy": "Delete"}
    number_of_snapshots = 1
    snapshot_object = scaleop.Snapshot(kubeconfig_value, test_namespace, keep_objects, value_pvc, value_vs_class,
                                       number_of_snapshots, data["image_name"], remote_data["id"], data["pluginNodeSelector"])
    ff.create_dir(remote_data["volDirBasePath"])


@pytest.mark.regression
def test_get_version():
    LOGGER.info("Remote Cluster Details:")
    LOGGER.info("-----------------------")
    ff.get_scale_version(remote_data)
    LOGGER.info("Local Cluster Details:")
    LOGGER.info("-----------------------")
    ff.get_scale_version(data)
    scaleop.get_kubernetes_version(kubeconfig_value)
    scaleop.scale_function.get_operator_image()
    scaleop.ob.get_driver_image()


@pytest.mark.regression
def test_snapshot_static_pass_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=True)


@pytest.mark.regression
def test_snapshot_static_multiple_snapshots():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=True, number_of_snapshots=3)


def test_snapshot_static_pass_3():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "gid": data["r_gid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_4():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_5():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_6():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "gid": data["r_gid_number"], "uid": data["r_uid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_7():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "gid": data["r_gid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_8():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_9():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "uid": data["r_uid_number"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_10():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_11():
    value_sc = {"volBackendFs": data["remoteFs"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "clusterId": data["remoteid"],
                "filesetType": "independent", "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_12():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "volBackendFs": data["remoteFs"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_13():
    value_sc = {"clusterId": data["remoteid"], "uid": data["r_uid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_14():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_15():
    value_sc = {"clusterId": data["remoteid"], "volBackendFs": data["remoteFs"],
                "gid": data["r_gid_number"], "uid": data["r_uid_number"],
                "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_static(value_sc, test_restore=True)


def test_snapshot_static_pass_16():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=False)


def test_snapshot_static_pass_17():
    value_sc = {"volBackendFs": data["remoteFs"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "clusterId": data["remoteid"],
                "filesetType": "independent", "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_static(value_sc, test_restore=False)


def test_snapshot_static_pass_18():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_static(value_sc, test_restore=False)


@pytest.mark.regression
def test_snapshot_dynamic_pass_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_vs_class={"deletionPolicy": "Retain"})


@pytest.mark.regression
def test_snapshot_dynamic_expected_fail_1():
    value_sc = {"volBackendFs": data["remoteFs"],
                "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=False, reason="Volume snapshot can only be created when source volume is independent fileset")


@pytest.mark.regression
def test_snapshot_dynamic_expected_fail_2():
    value_sc = {"volBackendFs": data["remoteFs"],
                "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_dynamic(value_sc, test_restore=False, reason="Volume snapshot can only be created when source volume is independent fileset")


@pytest.mark.regression
def test_snapshot_dynamic_multiple_snapshots():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, number_of_snapshots=3)


@pytest.mark.slow
def test_snapshot_dynamic_multiple_snapshots_256():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, number_of_snapshots=256)


@pytest.mark.slow
def test_snapshot_dynamic_multiple_snapshots_257():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, number_of_snapshots=257)


def test_snapshot_dynamic_pass_3():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "gid": data["r_gid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_4():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_5():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_6():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "gid": data["r_gid_number"], "uid": data["r_uid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_7():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "gid": data["r_gid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_8():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_9():
    value_sc = {"volBackendFs": data["remoteFs"],
                "clusterId": data["remoteid"], "uid": data["r_uid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_10():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_11():
    value_sc = {"volBackendFs": data["remoteFs"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "clusterId": data["remoteid"],
                "filesetType": "independent", "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_12():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "volBackendFs": data["remoteFs"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_13():
    value_sc = {"clusterId": data["remoteid"], "uid": data["r_uid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_14():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_15():
    value_sc = {"clusterId": data["remoteid"], "volBackendFs": data["remoteFs"],
                "gid": data["r_gid_number"], "uid": data["r_uid_number"],
                "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True)


def test_snapshot_dynamic_pass_16():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=False)


def test_snapshot_dynamic_pass_17():
    value_sc = {"volBackendFs": data["remoteFs"], "gid": data["r_gid_number"],
                "uid": data["r_uid_number"], "clusterId": data["remoteid"],
                "filesetType": "independent", "inodeLimit": data["r_inodeLimit"]}
    snapshot_object.test_dynamic(value_sc, test_restore=False)


def test_snapshot_dynamic_pass_18():
    value_sc = {"clusterId": data["remoteid"], "gid": data["r_gid_number"],
                "inodeLimit": data["r_inodeLimit"],
                "volBackendFs": data["remoteFs"]}
    snapshot_object.test_dynamic(value_sc, test_restore=False)


@pytest.mark.regression
def test_snapshot_dynamic_different_sc_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


@pytest.mark.regression
def test_snapshot_dynamic_different_sc_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_dynamic_different_sc_3():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_dynamic_different_sc_4():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_dynamic_different_sc_5():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_dynamic_different_sc_6():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_3():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_4():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"],
                "inodeLimit": data["r_inodeLimit"], "uid": data["r_uid_number"],
                "gid": data["r_gid_number"]}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_5():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_different_sc_6():
    value_sc = {"volBackendFs": data["remoteFs"],
                "inodeLimit": data["r_inodeLimit"],
                "clusterId": data["remoteid"], "filesetType": "independent"}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"]}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


@pytest.mark.regression
def test_snapshot_dynamic_nodeclass_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "GUI_MGMT_SERVERS"}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


@pytest.mark.regression
def test_snapshot_dynamic_nodeclass_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "GUI_SERVERS"}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_dynamic_nodeclass_3():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "randomnodeclassx"}
    restore_pvc = {"access_modes": "ReadWriteMany", "storage": "1Gi", "reason": "NotFound desc = nodeclass"}
    snapshot_object.test_dynamic(value_sc, test_restore=True, restore_sc=restore_sc, restore_pvc=restore_pvc)


def test_snapshot_static_nodeclass_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "GUI_MGMT_SERVERS"}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_nodeclass_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "GUI_SERVERS"}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc)


def test_snapshot_static_nodeclass_3():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    restore_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "nodeClass": "randomnodeclassx"}
    restore_pvc = {"access_modes": "ReadWriteMany", "storage": "1Gi", "reason": "NotFound desc = nodeclass"}
    snapshot_object.test_static(value_sc, test_restore=True, restore_sc=restore_sc, restore_pvc=restore_pvc)


def test_snapshot_dynamic_permissions_777_independent():
    LOGGER.warning("Testcase will fail if scale version < 5.1.1-4")
    value_pod = {"mount_path": "/usr/share/nginx/html/scale", "read_only": "False", "sub_path": ["sub_path_mnt"],
                 "volumemount_readonly": [False]}
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "permissions": "777",
                "gid": data["r_gid_number"], "uid": data["r_uid_number"]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_pod=value_pod)


def test_snapshot_dynamic_volume_expansion_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "allow_volume_expansion": True}
    value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi", "presnap_volume_expansion_storage": ["2Gi"],
                  "post_presnap_volume_expansion_storage": ["5Gi", "15Gi"], "postsnap_volume_expansion_storage": ["10Gi", "15Gi"]}]
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_pvc=value_pvc)


def test_snapshot_dynamic_volume_expansion_2():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "allow_volume_expansion": True}
    restore_sc = {"volBackendFs": data["remoteFs"],
                  "filesetType": "dependent", "clusterId": data["remoteid"], "allow_volume_expansion": True}
    value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi", "presnap_volume_expansion_storage": ["3Gi"],
                  "post_presnap_volume_expansion_storage": ["5Gi", "12Gi"], "postsnap_volume_expansion_storage": ["8Gi", "12Gi"]}]
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_pvc=value_pvc, restore_sc=restore_sc)


def test_snapshot_dynamic_volume_expansion_3():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"], "allow_volume_expansion": True}
    restore_sc = {"volBackendFs": data["remoteFs"], "volDirBasePath": data["r_volDirBasePath"],
                  "allow_volume_expansion": True}
    value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi", "presnap_volume_expansion_storage": ["2Gi"],
                  "post_presnap_volume_expansion_storage": ["5Gi", "15Gi"], "postsnap_volume_expansion_storage": ["10Gi", "15Gi"]}]
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_pvc=value_pvc, restore_sc=restore_sc)


def test_snapshot_dynamic_volume_cloning_1():
    value_sc = {"volBackendFs": data["remoteFs"], "clusterId": data["remoteid"]}
    value_pvc = [{"access_modes": "ReadWriteMany", "storage": "1Gi"}]
    value_clone_passed = {"clone_pvc": [{"access_modes": "ReadWriteMany", "storage": "1Gi"}, {"access_modes": "ReadWriteOnce", "storage": "1Gi"}]}
    snapshot_object.test_dynamic(value_sc, test_restore=True, value_pvc=value_pvc, value_clone_passed=value_clone_passed)