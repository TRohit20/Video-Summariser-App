import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart'; // Assuming the main.dart file is in the 'frontend' folder.

void main() {
  testWidgets('HomePage should render correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const YoutubeSummaryApp());

    expect(find.text('Summarizer'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
  });

  testWidgets('Entering video ID updates the text field',
      (WidgetTester tester) async {
    await tester.pumpWidget(const YoutubeSummaryApp());

    final videoIdField = find.byType(TextField);
    await tester.enterText(videoIdField, 'example_video_id');
    expect(find.text('example_video_id'), findsOneWidget);
  });
}
