import 'package:flutter/material.dart';
import 'package:flutter_django_auth_jwt/model/maintenance_model.dart';
import 'package:flutter_django_auth_jwt/service/api_service.dart';

class MaintenanceListScreen extends StatefulWidget {
  const MaintenanceListScreen({super.key});
  @override
  State<MaintenanceListScreen> createState() => _MaintenanceListScreenState();
}

class _MaintenanceListScreenState extends State<MaintenanceListScreen> {
  late Future<List<Maintenance>> futureMaintenance;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    futureMaintenance = ApiService().fetchMaintenances();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Maintenance'),
      ),
      body: FutureBuilder<List<Maintenance>>(
        future: futureMaintenance,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (snapshot.hasData) {
            return ListView.builder(
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(snapshot.data![index].name),
                  subtitle: (Text(snapshot.data![index].department)),
                  // Add other ListTile properties here
                );
              },
            );
          } else {
            return const Center(child: Text('No data available'));
          }
        },
      ),
    );
  }
}
