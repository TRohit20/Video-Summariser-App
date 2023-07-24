import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart'; // Assuming the main.dart file is in the 'frontend' folder.

void main() {
  testWidgets('HomePage should render correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const YoutubeSummaryApp());

    expect(find.text('Summarizer'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
    expect(find.byType(DropdownButton2), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
  });

  testWidgets('Entering video ID updates the text field',
      (WidgetTester tester) async {
    await tester.pumpWidget(const YoutubeSummaryApp());

    final videoIdField = find.byType(TextField);
    await tester.enterText(videoIdField, 'example_video_id');
    expect(find.text('example_video_id'), findsOneWidget);
  });

  testWidgets('Selecting video source updates the dropdown value',
      (WidgetTester tester) async {
    await tester.pumpWidget(const YoutubeSummaryApp());

    final dropdown = find.byType(DropdownButton2);
    await tester.tap(dropdown);
    await tester.pump();
    await tester.tap(find.text('VIMEO'));
    await tester.pump();
    expect(find.text('VIMEO'), findsOneWidget);
  });
}
