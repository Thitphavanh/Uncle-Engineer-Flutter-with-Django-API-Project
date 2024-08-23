import 'dart:convert';
import 'package:flutter_django_auth_jwt/model/maintenance_model.dart';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://localhost:8000/api";

  Future<List<Maintenance>> fetchMaintenances() async {
    final response = await http.get(Uri.parse('$baseUrl/all-maintenance'));

    if (response.statusCode == 200) {
      Map<String, dynamic> jsonResponse = json.decode(response.body);
      List<dynamic> data = jsonResponse['data'];
      List<Maintenance> maintenances =
          data.map((dynamic item) => Maintenance.fromJson(item)).toList();
      return maintenances;
    } else {
      throw Exception('Failed to load Maintenance');
    }
  }

  //  Future<List<Maintenance>> fetchMaintenances() async {
  //   final response = await http.get(Uri.parse(baseUrl));

  //   if (response.statusCode == 200) {
  //     List<dynamic> body = jsonDecode(response.body);
  //     List<Maintenance> maintenances = body.map((dynamic item) => Maintenance.fromJson(item)).toList();
  //     return maintenances;
  //   } else {
  //     throw Exception('Failed to load products');
  //   }
  // }

  // Future<Maintenance> getMaintenanceById(int? id) async {
  //   final response = await http.get(Uri.parse('$baseUrl/get/$id/'));

  //   print('Status Code: ${response.statusCode}');
  //   print('Response Body: ${response.body}');

  //   if (response.statusCode == 200) {
  //     try {
  //       return Maintenance.fromJson(jsonDecode(response.body));
  //     } catch (e) {
  //       throw Exception('Error parsing JSON: ${e.toString()}');
  //     }
  //   } else {
  //     throw Exception(
  //         'Failed to load Maintenance. Status Code: ${response.statusCode}');
  //   }
  // }

  Future<Maintenance> getMaintenanceById(int? id) async {
    final response = await http.get(Uri.parse('$baseUrl/maintenance/$id'));

    print('Status Code: ${response.statusCode}');
    print('Response Body: ${response.body}');

    if (response.statusCode == 200) {
      return Maintenance.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to load Maintenace');
    }
  }
}
