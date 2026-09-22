"""Small dependency-free reference for the official FedScale duration formula."""


def fedscale_completion_time(
    computation,
    communication,
    batch_size,
    local_steps,
    upload_size,
    download_size,
    augmentation_factor=3.0,
):
    return (
        augmentation_factor * batch_size * local_steps * float(computation) / 1000.0
        + (float(upload_size) + float(download_size)) / float(communication)
    )
