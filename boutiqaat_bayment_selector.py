import requests

def get_address_from_coordinates(latitude: float, longitude: float, language: str = "arabic") -> str:
    """
    Convert latitude and longitude to human-readable address using multiple geocoding services.
    """
    try:
        # Method 1: OpenStreetMap with multiple zoom levels
        for zoom_level in [18, 17, 16, 15]:  # Try different detail levels
            try:
                url = "https://nominatim.openstreetmap.org/reverse"
                params = {
                    'lat': latitude,
                    'lon': longitude,
                    'format': 'json',
                    'accept-language': 'ar' if language.lower() == "arabic" else 'en',
                    'zoom': zoom_level,
                    'addressdetails': 1,
                    'extratags': 1,
                    'namedetails': 1
                }
                
                headers = {'User-Agent': 'AlrawdatainWaterCompany/1.0'}
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Zoom {zoom_level} response: {data.get('display_name', 'No address')}")
                    
                    if 'address' in data:
                        # Try to build detailed address from components
                        detailed_addr = build_detailed_address(data['address'], language)
                        if detailed_addr and len(detailed_addr) > 20:  # Got meaningful details
                            return detailed_addr
                    
                    # Fallback to display_name for this zoom level
                    if 'display_name' in data and len(data['display_name']) > 10:
                        addr = data['display_name']
                        if language.lower() == "arabic":
                            addr = addr.replace('،', '، ')
                        return addr[:200] + "..." if len(addr) > 200 else addr
            
            except Exception as e:
                print(f"Zoom {zoom_level} error: {e}")
                continue
        
        # Method 2: Try to get nearby POIs or landmarks
        try:
            url = "https://nominatim.openstreetmap.org/search"
            # Search for nearby landmarks within 100m radius
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'limit': 5,
                'radius': 100,  # 100 meter radius
                'accept-language': 'ar' if language.lower() == "arabic" else 'en'
            }
            
            headers = {'User-Agent': 'AlrawdatainWaterCompany/1.0'}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                landmarks = response.json()
                if landmarks:
                    landmark_name = landmarks[0].get('display_name', '')
                    if landmark_name:
                        if language.lower() == "arabic":
                            return f"بالقرب من {landmark_name} (خط العرض: {latitude:.4f}، خط الطول: {longitude:.4f})"
                        else:
                            return f"Near {landmark_name} (Lat: {latitude:.4f}, Lon: {longitude:.4f})"
        
        except Exception as e:
            print(f"Landmark search error: {e}")
    
    except Exception as e:
        print(f"General geocoding error: {e}")
    
    # Final fallback with more precise coordinates
    if language.lower() == "arabic":
        return f"الموقع المحدد: {latitude:.6f}, {longitude:.6f}"
    else:
        return f"Precise Location: {latitude:.6f}, {longitude:.6f}"


def build_detailed_address(addr_components: dict, language: str) -> str:
    """Build detailed address from geocoding components."""
    try:
        address_parts = []
        
        if language.lower() == "arabic":
            # More comprehensive Arabic address building
            
            # Apartment/Unit details
            for key in ['unit', 'apartment', 'flat', 'suite']:
                if key in addr_components:
                    address_parts.append(f"شقة {addr_components[key]}")
                    break
            
            # Floor/Level
            for key in ['level', 'floor']:
                if key in addr_components:
                    address_parts.append(f"الطابق {addr_components[key]}")
                    break
            
            # Building details - try multiple keys
            building_parts = []
            for key in ['house_number', 'building', 'building_number']:
                if key in addr_components:
                    building_parts.append(f"مبنى {addr_components[key]}")
                    break
            
            # Street name - try multiple keys
            for key in ['road', 'street', 'pedestrian', 'path', 'way']:
                if key in addr_components:
                    building_parts.append(addr_components[key])
                    break
            
            if building_parts:
                address_parts.append("، ".join(building_parts))
            
            # Area details
            for key in ['neighbourhood', 'suburb', 'district', 'quarter', 'village']:
                if key in addr_components:
                    address_parts.append(f"منطقة {addr_components[key]}")
                    break
            
            # City/Governorate
            for key in ['city', 'town', 'municipality', 'state', 'county']:
                if key in addr_components:
                    address_parts.append(addr_components[key])
                    break
            
        else:
            # Comprehensive English address building
            
            # Apartment/Unit details
            for key in ['unit', 'apartment', 'flat', 'suite']:
                if key in addr_components:
                    address_parts.append(f"Unit {addr_components[key]}")
                    break
            
            # Floor/Level
            for key in ['level', 'floor']:
                if key in addr_components:
                    address_parts.append(f"Floor {addr_components[key]}")
                    break
            
            # Building and street
            building_parts = []
            for key in ['house_number', 'building', 'building_number']:
                if key in addr_components:
                    building_parts.append(addr_components[key])
                    break
            
            for key in ['road', 'street', 'pedestrian', 'path', 'way']:
                if key in addr_components:
                    building_parts.append(addr_components[key])
                    break
            
            if building_parts:
                address_parts.append(" ".join(building_parts))
            
            # Area details
            for key in ['neighbourhood', 'suburb', 'district', 'quarter', 'village']:
                if key in addr_components:
                    address_parts.append(addr_components[key])
                    break
            
            # City/State
            for key in ['city', 'town', 'municipality', 'state', 'county']:
                if key in addr_components:
                    address_parts.append(addr_components[key])
                    break
        
        # Join and return
        if address_parts:
            separator = "، " if language.lower() == "arabic" else ", "
            return separator.join(address_parts)
    
    except Exception as e:
        print(f"Address building error: {e}")
    
    return ""


def parse_coordinates(delivery_address: str) -> tuple:
    """
    Parse coordinates from delivery address string.
    
    Args:
        delivery_address: Address string that may contain coordinates
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if parsing fails
    """
    if not delivery_address:
        return None, None
    
    try:
        print(f"Parsing address: {delivery_address}")  # Debug log
        
        # Clean the input string
        address = delivery_address.strip()
        
        # Handle comma-separated coordinates (most common format)
        if ',' in address:
            parts = address.split(',')
            if len(parts) >= 2:
                # Try to find numeric parts that look like coordinates
                for i in range(len(parts)-1):
                    try:
                        lat_str = parts[i].strip()
                        lon_str = parts[i+1].strip()
                        
                        # Remove any non-numeric characters except dots and minus
                        import re
                        lat_clean = re.sub(r'[^\d.-]', '', lat_str)
                        lon_clean = re.sub(r'[^\d.-]', '', lon_str)
                        
                        if lat_clean and lon_clean:
                            lat = float(lat_clean)
                            lon = float(lon_clean)
                            
                            print(f"Extracted coordinates: lat={lat}, lon={lon}")  # Debug log
                            
                            # Validate coordinates (global range, but we'll focus on Kuwait)
                            if -90 <= lat <= 90 and -180 <= lon <= 180:
                                # For Kuwait specifically (optional validation)
                                if 28.0 <= lat <= 31.0 and 46.0 <= lon <= 49.0:
                                    print(f"Valid Kuwait coordinates found: {lat}, {lon}")
                                    return lat, lon
                                else:
                                    # Still valid coordinates, just not Kuwait
                                    print(f"Valid coordinates found (not Kuwait): {lat}, {lon}")
                                    return lat, lon
                    except (ValueError, IndexError):
                        continue
        
        # Handle space-separated coordinates
        elif ' ' in address:
            parts = address.split()
            for i in range(len(parts)-1):
                try:
                    lat_str = parts[i].strip()
                    lon_str = parts[i+1].strip()
                    
                    # Remove any non-numeric characters except dots and minus
                    import re
                    lat_clean = re.sub(r'[^\d.-]', '', lat_str)
                    lon_clean = re.sub(r'[^\d.-]', '', lon_str)
                    
                    if lat_clean and lon_clean:
                        lat = float(lat_clean)
                        lon = float(lon_clean)
                        
                        print(f"Extracted coordinates from space-separated: lat={lat}, lon={lon}")
                        
                        if -90 <= lat <= 90 and -180 <= lon <= 180:
                            return lat, lon
                except (ValueError, IndexError):
                    continue
        
        # Try to extract numbers that might be coordinates from any format
        import re
        numbers = re.findall(r'-?\d+\.?\d*', address)
        if len(numbers) >= 2:
            for i in range(len(numbers)-1):
                try:
                    lat = float(numbers[i])
                    lon = float(numbers[i+1])
                    
                    print(f"Extracted from regex: lat={lat}, lon={lon}")
                    
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        return lat, lon
                except ValueError:
                    continue
    
    except Exception as e:
        print(f"Coordinate parsing error: {e}")
    
    print("No valid coordinates found in the address string")
    return None, None


def main(conversationId:str, language: str = "english", total_amount: str = "", delivery_address: str = "", building_number: str = "", department_number: str = "") -> dict:
    """
    Send payment method selection options to customer with address geocoding.

    Args:
        phone_number: The recipient's phone number in international format (e.g., "+201033505065")
        language: Selected language ("english" or "arabic")
        total_amount: Total order amount including delivery (optional)
        delivery_address: Delivery address (coordinates will be converted to readable address)
        building_number: Building number (optional)
        department_number: Apartment/Department number (optional)

    Returns:
        dict: The API response with success message
    """
    # WhatsApp API endpoint
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/interactive"
    # Authorization header with your token
    headers = {
        "Authorization": "Bearer So+MR00BCG1dpI+EMkOiwDcQbBxUIxdcC9kwGof/zhc9vtyDtMAWpMqEs/fdzPMVCX2CBCe4dXo8J0nsLWGWOZwJnFe/UfSqJ7fqNjZ6Iq/1koVlRePxtwRa2mcbImN/0zwelBhcs4eJ32nSCqk1+IFb705/F3xT2BNNWPAZsK9DxNzi4Serm1gVxyr9CA==",
        "Content-Type": "application/json"
    }

    # Convert coordinates to readable address if needed
    readable_address = delivery_address
    if delivery_address:
        lat, lon = parse_coordinates(delivery_address)
        if lat is not None and lon is not None:
            readable_address = get_address_from_coordinates(lat, lon, language)
            print(f"Converted coordinates ({lat}, {lon}) to address: {readable_address}")
    
    # Add building and apartment details to the address
    if readable_address and (building_number or department_number):
        address_suffix = []
        
        if language.lower() == "arabic":
            # Arabic format
            if building_number:
                address_suffix.append(f"عمارة رقم {building_number}")
            if department_number:
                address_suffix.append(f"شقة رقم {department_number}")
            
            if address_suffix:
                readable_address = f"{readable_address}، {' ، '.join(address_suffix)}"
        else:
            # English format
            if building_number:
                address_suffix.append(f"Building No. {building_number}")
            if department_number:
                address_suffix.append(f"Apartment No. {department_number}")
            
            if address_suffix:
                readable_address = f"{readable_address}, {', '.join(address_suffix)}"
        
        print(f"Final address with building details: {readable_address}")

    # Define content based on language
    if language.lower() == "arabic":
        header_text = "💳 اختيار طريقة الدفع"
        if total_amount and readable_address:
            body_text = f"📍 عنوان التوصيل: {readable_address}\n💰 المبلغ الإجمالي: {total_amount} دينار كويتي\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        elif total_amount:
            body_text = f"💰 المبلغ الإجمالي: {total_amount} دينار كويتي\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        elif readable_address:
            body_text = f"📍 عنوان التوصيل: {readable_address}\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        else:
            body_text = "يرجى اختيار طريقة الدفع المفضلة لديك:"
        footer_text = "آمن ومضمون"
        buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": "payment_knet",
                    "title": "💳 كي نت (K-Net)"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "payment_credit",
                    "title": "💳 بطاقة ائتمان"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "payment_cash",
                    "title": "💵 الدفع نقداً"
                }
            }
        ]
    else:
        header_text = "💳 Payment Method Selection"
        if total_amount and readable_address:
            body_text = f"📍 Delivery Address: {readable_address}\n💰 Total Amount: {total_amount} KWD\n\nPlease select your preferred payment method:"
        elif total_amount:
            body_text = f"💰 Total Amount: {total_amount} KWD\n\nPlease select your preferred payment method:"
        elif readable_address:
            body_text = f"📍 Delivery Address: {readable_address}\n\nPlease select your preferred payment method:"
        else:
            body_text = "Please select your preferred payment method:"
        footer_text = "Secure & Safe"
        buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": "payment_knet",
                    "title": "💳 K-Net"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "payment_credit",
                    "title": "💳 Credit Card"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "payment_cash",
                    "title": "💵 Cash on Delivery"
                }
            }
        ]

    # Payload for payment selection
    payload = {
        "interactive_type": "quick_reply",
  "body_text": body_text,
  "header_text": header_text,
  "footer_text": footer_text,
  "quick_reply_config": {
    "quick_reply_buttons":buttons
  }
    }

    # Send the request
    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)

    try:
        result = response.json()
        print("Response JSON:", result)
        
        # Return success message based on language
        if response.status_code == 200:
            success_message = ""
            if language.lower() == "arabic":
                success_message = f"تم إرسال خيارات الدفع بنجاح 💳\nالعنوان: {readable_address if readable_address else 'غير محدد'}"
            else:
                success_message = f"Payment options sent successfully 💳\nAddress: {readable_address if readable_address else 'Not specified'}"
            
            return {
                "result": success_message,
                "status": "success",
                "converted_address": readable_address,
                "building_number": building_number,
                "department_number": department_number
            }
        else:
            return {
                "result": f"Error sending message: HTTP {response.status_code}",
                "status": "error",
                "status_code": response.status_code
            }
            
    except ValueError:
        error_msg = f"Invalid JSON response: {response.text}"
        print(error_msg)
        return {
            "result": error_msg,
            "status": "error",
            "error_type": "json_parsing"
        }
    except Exception as e:
        error_msg = f"Request failed: {str(e)}"
        print(error_msg)
        return {
            "result": error_msg,
            "status": "error",
            "error_type": "request_failed"
        }