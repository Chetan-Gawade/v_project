from .inception_resnet_v1 import InceptionResnetV1
import torch
import cv2


DEVICE = "cpu"
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_model(weights_path: str) -> InceptionResnetV1:
    model = InceptionResnetV1(device=DEVICE)  # Load in CPU mode no GPU on server
    model.load_state_dict(torch.load(weights_path), strict=False)  # Load Model
    model.eval()

    return model


def load_fd_model() -> cv2.CascadeClassifier:
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    return face_cascade


def preprocess_image(image: cv2.Mat, detector) -> torch.Tensor:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale

    faces = detector.detectMultiScale(  # Perform Face detection
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    if len(faces) == 0:  # No faces the input is not valid
        raise ValueError("No face detected in the image.")

    if len(faces) >= 2:  # We cannot have more than 1 person in frame
        raise RuntimeError("Multiple faces in the input image")

    x, y, w, h = faces[0]  # Take 1st Face
    cropped = image[y : y + h, x : x + w]  # Crop
    cropped = cv2.cvtColor(
        cropped, cv2.COLOR_BGR2RGB
    )  # CNN expects RGB input as (160, 160)
    cropped = cv2.resize(cropped, (160, 160))

    # Normalize image (pytorch requirement) (setup)
    cropped = cropped / 255.0
    mean = torch.tensor([0.485, 0.456, 0.406], device=DEVICE)
    std = torch.tensor([0.229, 0.224, 0.225], device=DEVICE)

    # Convert to torch tensor
    cropped_tensor = torch.tensor(cropped, dtype=torch.float32, device=DEVICE)
    cropped_tensor = (cropped_tensor - mean) / std  # Perform normalization

    final = cropped_tensor.permute(2, 0, 1).unsqueeze(
        0
    )  # Torch expects images in (Channels, Height, Width)

    return final

def predict(
    model: InceptionResnetV1, profile: cv2.Mat, other_images: list[cv2.Mat], detector
) -> list[float]:
    profile_processed = preprocess_image(
        profile, detector
    )  # Process the profile image (we compare all images to profile)
    profile_emb = model(
        profile_processed
    ).squeeze()  # Generate embedding vector for profile image

    # process and concatenate all other images into 1 tensor batch
    other = torch.cat(tuple(map(lambda x: preprocess_image(x, detector), other_images)))
    other_emb = model(other)  # get embedding vector for other images

    return (
        torch.nn.functional.cosine_similarity(profile_emb, other_emb)
        .detach()
        .cpu()
        .tolist()
    )  # Should keep threshold of at least 80%
