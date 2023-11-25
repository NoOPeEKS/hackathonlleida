from django.shortcuts import render
import requests

# Create your views here.


def api_vision(request):
    if request.method == 'POST':
        result = request.POST.copy()

        url_img = result.get('input', None)

        url = 'https://api-us.restb.ai/vision/v2/multipredict'
        payload = {
            # Add your client key
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a',
            'model_id': 're_roomtype_global_v2,re_exterior_styles,re_features_v5,re_condition_r1r6_global,re_condition_c1c6,re_inspection_damage',
            # Add the image URL you want to process
            'image_url': url_img
        }

        # Make the API request
        response = requests.get(url, params=payload)

        response_json = response.json()

        exterior_style = response_json['response']['solutions']['re_exterior_styles']['top_prediction']['label']
        room_type = response_json['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']
        r1r6 = response_json['response']['solutions']['re_condition_r1r6_global']['score']
        c1c6 = response_json['response']['solutions']['re_condition_c1c6']['score']
        detections = response_json['response']['solutions']['re_features_v5']['detections']
        feature_labels = [detection['label'] for detection in detections]

        return render(request, 'api_vision.html', {'exterior_style': exterior_style, 'room_type': room_type,
                                                   'r1r6': r1r6, 'c1c6': c1c6, 'feature_labels': feature_labels,
                                                   'link_img': url_img})

    return render(request, 'api_vision.html', {})


def api_description(request):
    if request.method == 'POST':
        result = request.POST.copy()

        property_type = result.get('property_type', None)
        adress = result.get('adress', None)
        city = result.get('city', None)
        state = result.get('state', None)
        country = result.get('country', None)
        image_url = result.get('image_url', None)

        url = 'https://description.restb.ai/v2/describe/listing'
        payload = {
            # Add your client key
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

        # Make the classify request
        response = requests.post(url, params=payload, json=request_body)

        # The response is formatted in JSON
        json_response = response.json()

        descriptions = json_response['response']['description_blocks']

        final_desc = str()

        for block in descriptions:
            final_desc += block['description'] + ' '

        return render(request, 'api_description.html', {'description': final_desc, 'link_img': image_url})

    return render(request, 'api_description.html', {})


def api_property(request):
    if request.method == 'POST':
        result = request.POST.copy()

        url_img = result.get('input', None)
        url_list = list()

        if ',' in url_img:
            url_list = url_img.split(',')

        else:
            url_list = [url_img]

        url = 'https://property.restb.ai/v1/multianalyze'
        payload = {
            # Add your client key
            'client_key': 'b1df17d9f440b1a56f07936fb84c56039d4374c86c91618a938e465e8194876a',
        }

        request_body = {
            "image_urls": url_list,
            "solutions": {"roomtype": 1.0, "roomtype_reso": 1.0, "style": 1.0, "r1r6": None, "c1c6": None, "q1q6": None,
                          "features": 5.0, "features_reso": 2.0, "compliance": 3.0, "caption": None}
        }
        # Make the API request
        response = requests.post(url, params=payload, json=request_body)

        response_json = response.json()

        return render(request, 'api_property.html', {'output': response_json})

    return render(request, 'api_property.html', {})


def api_intelligence(request):
    if request.method == 'POST':
        result = request.POST.copy()

        adress = result.get('adress', None)
        city = result.get('city', None)
        postal_code = result.get('postal_code', None)
        state = result.get('state', None)
        country = result.get('country', None)



        url = 'https://intelligence.restb.ai/v1/search/comparables'
        payload = {
            # Add your client key
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

        # Make the classify request
        response = requests.post(url, params=payload, json=request_body)

        # The response is formatted in JSON
        json_response = response.json()

        return render(request, 'api_intelligence.html', {'output': json_response})

    return render(request, 'api_intelligence.html', {})


def home(request):
    return render(request, 'home.html', {})
