"""NYC Taxi Duration Prediction Web Service

Flask API for predicting NYC taxi trip duration using a linear regression model.
This service loads a pre-trained model and exposes a REST endpoint for predictions.

Author: MLOps Team
Version: 1.0
"""

import pickle
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and DictVectorizer at application startup
try:
    with open('lin_reg.bin', 'rb') as f_in:
        logger.info('🔄 Loading model and DictVectorizer...')
        (dv, model) = pickle.load(f_in)
        logger.info('✅ Model and DV loaded successfully')
except FileNotFoundError:
    logger.error('❌ Error: lin_reg.bin file not found')
    raise
except Exception as e:
    logger.error(f'❌ Error loading model: {e}')
    raise


def prepare_features(ride):
    """
    Prepare features needed for prediction from trip data.
    
    Args:
        ride (dict): Dictionary with trip data that must contain:
            - PULocationID (int): Pickup zone ID
            - DOLocationID (int): Dropoff zone ID  
            - trip_distance (float): Trip distance in miles
    
    Returns:
        dict: Dictionary with processed features:
            - PU_DO (str): Pickup-dropoff combination as string
            - trip_distance (float): Trip distance
    
    Example:
        >>> ride = {
        ...     'PULocationID': 161,
        ...     'DOLocationID': 236,
        ...     'trip_distance': 2.5
        ... }
        >>> features = prepare_features(ride)
        >>> print(features)
        {'PU_DO': '161_236', 'trip_distance': 2.5}
    """
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    logger.info(f"✅ Features prepared: PU_DO={features['PU_DO']}, distance={features['trip_distance']}")
    return features


def predict(features):
    """
    Perform duration prediction using the loaded model.
    
    Args:
        features (dict): Features prepared with prepare_features()
    
    Returns:
        float: Predicted trip duration in minutes
    
    Note:
        - Uses DictVectorizer to transform categorical features
        - Applies pre-trained linear regression model
        - Returns prediction as float for JSON serialization
    
    Example:
        >>> features = {'PU_DO': '161_236', 'trip_distance': 2.5}
        >>> duration = predict(features)
        >>> print(f"Predicted duration: {duration:.2f} minutes")
    """
    X = dv.transform(features)
    preds = model.predict(X)
    predicted_duration = float(preds[0])
    logger.info(f"🎯 Prediction made: {predicted_duration:.2f} minutes")
    return predicted_duration


# Create Flask application
app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    REST endpoint for taxi trip duration prediction.
    
    Method: POST
    Content-Type: application/json
    
    Request Body:
        {
            "PULocationID": int,      # Pickup zone ID (1-263)
            "DOLocationID": int,      # Dropoff zone ID (1-263) 
            "trip_distance": float    # Distance in miles
        }
    
    Response:
        {
            "duration": float         # Predicted duration in minutes
        }
    
    Returns:
        JSON response with predicted duration or 400/500 error
    
    Example:
        curl -X POST http://localhost:9696/predict \
             -H "Content-Type: application/json" \
             -d '{"PULocationID": 161, "DOLocationID": 236, "trip_distance": 2.5}'
        
        Response: {"duration": 12.34}
    """
    try:
        # Get JSON data from request
        ride = request.get_json()
        
        if not ride:
            logger.error("❌ Request without JSON data")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['PULocationID', 'DOLocationID', 'trip_distance']
        for field in required_fields:
            if field not in ride:
                logger.error(f"❌ Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        logger.info(f"🚕 New prediction: {ride['PULocationID']} -> {ride['DOLocationID']}")
        
        # Prepare features and predict
        features = prepare_features(ride)
        pred = predict(features)
        
        result = {
            'duration': pred,
            'pickup_location': ride['PULocationID'],
            'dropoff_location': ride['DOLocationID'],
            'trip_distance': ride['trip_distance']
        }
        
        logger.info(f"✅ Response sent: {pred:.2f} minutes")
        return jsonify(result)
        
    except KeyError as e:
        logger.error(f"❌ Missing field in request: {e}")
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"❌ Error in prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        JSON response with service status
    
    Example:
        curl http://localhost:9696/health
        
        Response: {"status": "healthy", "model_loaded": true}
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'dv_loaded': dv is not None,
        'service': 'NYC Taxi Duration Prediction'
    })


if __name__ == "__main__":
    """
    Main entry point to run the Flask server.
    
    Configuration:
        - Debug: True (development only)
        - Host: 0.0.0.0 (accepts external connections)
        - Port: 9696
    """
    logger.info("🚀 Starting Flask server on port 9696...")
    app.run(debug=True, host='0.0.0.0', port=9696)
