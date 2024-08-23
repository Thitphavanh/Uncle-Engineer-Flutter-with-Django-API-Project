import 'package:flutter/material.dart';
import 'package:flutter_django_auth_jwt/screen/maintenance_detail_screen.dart';

import 'screen/maintenance_list_screen.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: MaintenanceDetailScreen(maintenanceId: 1),
      // home: MaintenanceListScreen(),
    );
  }
}
