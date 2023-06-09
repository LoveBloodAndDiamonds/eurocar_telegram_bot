from bot.models import TextNames as Tn


def generate_preview_text(state_data: dict, additional_text: str = '', ignore: list = None) -> str:
    """
    Generate text to preview what user choose from region to car_model
    :param state_data: dict with state data
    :param ignore: keys what func will ignore and dont add
    :param additional_text: additional text before \n
    :return:
    """
    text = str()
    keys = [key for key in state_data if key not in ignore] if ignore else [key for key in state_data if key]
    for key in keys:
        match key:
            case "REGION":
                text += Tn.R.format(state_data[key])
            case "START_DATE":
                text += Tn.S.format(state_data[key])
            case "END_DATE":
                text += Tn.E.format(state_data[key])
            case "RENT_DAYS":
                text += Tn.D.format(state_data[key])
            case "CAR_CLASS":
                text += Tn.C.format(state_data[key][1])
            case "CAR_MODEL":
                text += Tn.M.format(state_data[key][0])
            case "RENT_PRICE":
                text += Tn.T.format(state_data[key])

    return text + additional_text + '\n'
