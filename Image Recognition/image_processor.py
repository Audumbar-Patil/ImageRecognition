import os
import logging
import io
from PIL import Image
import torch
from torchvision import models, transforms
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        try:
            logger.info("Initializing ResNet model...")
            # Load pretrained ResNet model with explicit weights parameter
            weights = models.ResNet50_Weights.DEFAULT
            self.model = models.resnet50(weights=weights)
            self.model.eval()  # Set to evaluation mode

            # Get class mapping from the weights
            self.categories = weights.meta["categories"]
            logger.info(f"Loaded {len(self.categories)} categories")

            # Define image transforms using the same preprocessing as the weights
            self.transform = weights.transforms()

            logger.info("Model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ImageProcessor: {str(e)}")
            raise

    def process_image(self, file) -> List[Dict[str, float]]:
        try:
            logger.debug("Starting image processing")
            # Read and preprocess the image
            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes))

            # Convert to RGB if necessary
            if img.mode != 'RGB':
                logger.debug(f"Converting image from {img.mode} to RGB")
                img = img.convert('RGB')

            # Apply transformations
            logger.debug("Applying image transformations")
            input_tensor = self.transform(img)
            input_batch = input_tensor.unsqueeze(0)

            # Get predictions
            logger.debug("Running prediction")
            with torch.no_grad():
                output = self.model(input_batch)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)

            # Get top 5 predictions
            top5_prob, top5_catid = torch.topk(probabilities, 5)
            results = []

            logger.debug(f"Processing top 5 predictions")
            for i in range(top5_prob.size(0)):
                label = self.categories[top5_catid[i]]
                confidence = float(top5_prob[i] * 100)
                results.append({
                    'label': label,
                    'confidence': confidence
                })
                logger.debug(f"Prediction {i+1}: {label} ({confidence:.2f}%)")

            logger.info(f"Successfully processed image. Found {len(results)} predictions.")
            return results

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise