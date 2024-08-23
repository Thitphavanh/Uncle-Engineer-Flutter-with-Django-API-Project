import 'package:flutter/material.dart';

import 'model/maintenance_model.dart';
import 'screen/maintenance_list_screen.dart';
import 'service/api_service.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ตาราง แจ้งซ้อม')),
      // Geting Future data from API
      body: FutureBuilder<List<Maintenance>>(
        future: ApiService().fetchMaintenances(),
        builder:
            (BuildContext context, AsyncSnapshot<List<Maintenance>> snapshot) {
          if (!snapshot.hasData) {
            // checking if API has data & if no data then loading bar
            return const Center(child: CircularProgressIndicator());
          } else {
            // return data after recieving it in snapshot.
            return Container(
                padding: const EdgeInsets.all(5),
                // Data Table logic and code is in DataClass
                child: MaintenanceListScreen(
                    maintenances: snapshot.data as List<Maintenance>));
          }
        },
      ),
    );
  }
}
