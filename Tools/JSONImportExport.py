def ExportBlockArchitectureToJSON(ba, path):

    import json

    with open("{}/ba.json".format(path), "w+") as f:
        ba_dict = ba.toJSON()
        json.dump(ba_dict, f)


def ImportBlockArchitectureFromJSON(ba_json_loc):
    import json

    with open(ba_json_loc, "r") as f:
        ba = json.load(f)

        from TensorNAS.Core.Block import get_block_from_JSON

        ba = get_block_from_JSON(ba)

        return ba
    return None


def ImportGeneration(gen_folder):
    from os import listdir

    ind_folders = listdir(gen_folder)

    models = []

    for folder in ind_folders:
        models.append(
            ImportBlockArchitectureFromJSON("{}/{}/ba.json".format(gen_folder, folder))
        )

    return models


def GetBlockMod(blk_name):
    import TensorNAS, os, glob

    framework_dir = os.path.dirname(os.path.dirname(TensorNAS.__file__))
    framework_path = os.path.abspath(os.path.dirname(TensorNAS.__file__))
    try:
        mod_name = glob.glob(
            "{}/**/{}.py".format(framework_path, blk_name),
            recursive=True,
        )
        mod_name = mod_name[0][len(framework_dir + "/") : -3].replace("/", ".")
    except Exception as e:
        raise Exception(
            "Block Architecture module not found, is the correct one specified in test config? '{}'".format(
                e
            )
        )

    import importlib

    print("Importing block module: {}".format(mod_name))

    mod = importlib.import_module(mod_name)

    return mod
