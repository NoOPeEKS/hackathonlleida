from django.shortcuts import render
import requests

import pandas as pd
from collections import ChainMap

# Create your views here.

def get_dataframe(json_object):
    """
    Creates a Pandas DataFrame from a JSON object containing comparables.

    Args:
    - json_object (dict): A JSON object containing comparables data.

    Returns:
    - pd.DataFrame: A Pandas DataFrame constructed from the JSON data.
    """

    # Extract the comparables from the json and group by keys
    data_list = json_object['response']['comparables']
    grouped_dict = dict()
    [grouped_dict.setdefault(key, []).append(value) for d in data_list for key, value in d.items()]
    
    # Store ordered data
    ordered_dict = {}
    for key, value in grouped_dict.items():
        for i, inner_dict in enumerate(value):
            # Skip media, not useful in this case
            if key == 'media':
                continue
            ordered_dict.setdefault(i, []).append(inner_dict)

    # Merge inner dictionaries
    final_dict = {}
    for key, value in ordered_dict.items():
        final_dict[key] = dict(ChainMap(*value))

    return pd.DataFrame.from_dict(final_dict).T


def api_vision(request):
    """
    Handles POST requests to perform image recognition using a vision API.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'api_vision.html' template with recognition results if successful, 
                    otherwise renders the same template without display.
    """

    # Get request data
    if request.method == 'POST':
        result = request.POST.copy()

        url_img = result.get('input', None)
        
        # Prepare API request payload
        url = 'https://api-us.restb.ai/vision/v2/multipredict'
        payload = {
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a',
            'model_id': 're_roomtype_global_v2,re_exterior_styles,re_features_v5,re_condition_r1r6_global,re_condition_c1c6,re_inspection_damage',
            'image_url': url_img
        }

        response = requests.get(url, params=payload)

        response_json = response.json()
        
        # Extract final params from API response
        exterior_style = response_json['response']['solutions']['re_exterior_styles']['top_prediction']['label']
        room_type = response_json['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']
        r1r6 = response_json['response']['solutions']['re_condition_r1r6_global']['score']
        c1c6 = response_json['response']['solutions']['re_condition_c1c6']['score']
        detections = response_json['response']['solutions']['re_features_v5']['detections']
        feature_labels = [detection['label'] for detection in detections]
        
        # Render the template with API parameter results
        return render(request, 'api_vision.html', {'exterior_style': exterior_style, 'room_type': room_type,
                                                   'r1r6': r1r6, 'c1c6': c1c6, 'feature_labels': feature_labels,
                                                   'link_img': url_img, 'display': True})

    return render(request, 'api_vision.html', {'display': False})


def api_description(request):
    """
    Handles POST requests to retrieve property description using an API.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'api_description.html' template with property descriptions if successful,
                    otherwise renders an empty template.
    """

    # Get request data
    if request.method == 'POST':
        result = request.POST.copy()

        property_type = result.get('property_type', None)
        adress = result.get('adress', None)
        city = result.get('city', None)
        state = result.get('state', None)
        country = result.get('country', None)
        image_url = result.get('image_url', None)
        

        # Define API endpoint, payload and request body
        url = 'https://description.restb.ai/v2/describe/listing'
        payload = {
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a'
        }
        request_body = {
            "property": {
                "property_type": property_type,
            },
            "location": {
                "address": adress,
                "city": city,
                "state": state,
                "country": country
            },
            "image": [{"url": image_url}]
        }

        response = requests.post(url, params=payload, json=request_body)

        json_response = response.json()
        
        # Retrieve the descriptions and join them for a final description
        descriptions = json_response['response']['description_blocks']

        final_desc = str()

        for block in descriptions:
            final_desc += block['description'] + ' '
        
        # Render the description and image
        return render(request, 'api_description.html', {'description': final_desc, 'link_img': image_url})

    return render(request, 'api_description.html', {})


def api_property(request):
    """
    Handles POST requests to analyze property images using an API.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'api_property.html' template with property analysis results if successful,
                    otherwise renders an empty template.
    """

    # Get the request values
    if request.method == 'POST':
        result = request.POST.copy()

        url_img = result.get('input', None)

        if ',' in url_img:
            url_list = url_img.split(',')

        else:
            url_list = [url_img]
        
        # Prepare request payload and request body
        url = 'https://property.restb.ai/v1/multianalyze'
        payload = {
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a',
        }

        request_body = {
            "image_urls": url_list,
            "solutions": {"roomtype": 1.0, "roomtype_reso": 1.0, "style": 1.0, "r1r6": None, "c1c6": None, "q1q6": None,
                          "features": 5.0, "features_reso": 2.0, "compliance": 3.0, "caption": None}
        }
        response = requests.post(url, params=payload, json=request_body)

        response_json = response.json()
        
        # Extract the parameters from the response json
        c1c6_global_score = response_json["response"]["solutions"]["c1c6"]["property"]["score"]
        c1c6_individual_scores = response_json["response"]["solutions"]["c1c6"]["summary"]["score"]

        features_labels = [detection["label"] for result in response_json["response"]["solutions"]["features"]["results"]
                           for detection in result["values"]["detections"]]

        features_reso_labels = [item["label"] for item in
                                response_json["response"]["solutions"]["features_reso"]["summary"]["lookup_fields"]]

        q1q6_global_score = response_json["response"]["solutions"]["q1q6"]["property"]["score"]
        q1q6_individual_scores = response_json["response"]["solutions"]["q1q6"]["summary"]["score"]

        r1r6_global_score = response_json["response"]["solutions"]["r1r6"]["property"]["score"]
        r1r6_individual_scores = response_json["response"]["solutions"]["r1r6"]["summary"]["score"]

        roomtype_top_prediction = [result["values"]["top_prediction"] for result in
                                   response_json["response"]["solutions"]["roomtype"]["results"]]
        roomtype_reso_top_prediction = [result["values"]["top_prediction"] for result in
                                        response_json["response"]["solutions"]["roomtype_reso"]["results"]]

        style_info_available = "style" in response_json["response"]["solutions"]
        
        # Create a dataframe to easily render in html
        data = {'c1c6_global': c1c6_global_score, 'c1c6_indiv': c1c6_individual_scores,
                 'features_labels': features_labels, 'features_reso_labels': features_reso_labels,
                 'q1q6_global': q1q6_global_score, 'q1q6_indiv': q1q6_individual_scores,
                 'r1r6_global': r1r6_global_score, 'r1r6_indiv': r1r6_individual_scores,
                 'roomtype_pred': roomtype_top_prediction, 'roomtype_reso_pred': roomtype_reso_top_prediction,
                 'style_info': style_info_available}

        df = pd.DataFrame([data])
        
        # Render the dataframe on the template
        context = {'data': df.to_html(classes='table table-striped', border=0)}
        return render(request, 'api_property.html', context)

    return render(request, 'api_property.html', {})


def api_intelligence(request):
   """
    Handles POST requests to search for comparables using an intelligence API.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'api_intelligence.html' template with comparable data in a table if successful,
                    otherwise renders an empty template.
    """

    # Process request parameters and extract them.
    if request.method == 'POST':
        result = request.POST.copy()

        adress = result.get('adress', None)
        city = result.get('city', None)
        postal_code = result.get('postal_code', None)
        state = result.get('state', None)
        country = result.get('country', None)


        # Prepare API request payload and request body
        url = 'https://intelligence.restb.ai/v1/search/comparables'
        payload = {
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a'
        }
        request_body = {
            "location": {
                "street_address": adress,
                "city": city,
                "postal_code": postal_code,
                "state": state,
                "country": country
            }
        }

        response = requests.post(url, params=payload, json=request_body)

        json_response = response.json()
        
        # Put the response of the API Request into a dataframe to easily render it
        dataframe = get_dataframe(json_response)

        data = {
            'table': dataframe.to_html(classes='table table-striped', border=0)
        }
        
        # Render the dataframe on the template
        return render(request, 'api_intelligence.html', data)

    return render(request, 'api_intelligence.html', {})


def home(request):
    return render(request, 'home.html', {})
