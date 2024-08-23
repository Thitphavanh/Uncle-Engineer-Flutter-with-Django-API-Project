import 'package:flutter/material.dart';
import 'package:flutter_django_auth_jwt/model/maintenance_model.dart';
import 'package:flutter_django_auth_jwt/service/api_service.dart';

class MaintenanceDetailScreen extends StatefulWidget {
  final int maintenanceId;

  const MaintenanceDetailScreen({Key? key, required this.maintenanceId}) : super(key: key);
      // Receive the maintenance ID as a parameter

  @override
  State<MaintenanceDetailScreen> createState() =>
      _MaintenanceDetailScreenState();
}

class _MaintenanceDetailScreenState extends State<MaintenanceDetailScreen> {
  late Future<Maintenance> futureMaintenance;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    futureMaintenance =
          ApiService().getMaintenanceById(widget.maintenanceId);
    
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('Maintenance Details'),
        ),
        body: FutureBuilder<Maintenance>(
          future: futureMaintenance,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            } else if (!snapshot.hasData) {
              return const Center(child: Text('No data available'));
            } else {
              final maintenance = snapshot.data!;
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('ID: ${maintenance.id}'),
                    Text('Name: ${maintenance.name}'),
                    Text('Department: ${maintenance.department}'),
                    Text('Machine: ${maintenance.machine}'),
                    Text('Proplem: ${maintenance.proplem}'),
                    Text('Tel: ${maintenance.tel}'),
                  ],
                ),
              );
            }
          },
        ));
  }
}
