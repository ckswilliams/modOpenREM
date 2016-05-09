def average_chart_inc_histogram_data(database_events, db_display_name_relationship, db_series_names, db_value_name,
                                     value_multiplier, plot_average, plot_freq, plot_series_per_system,
                                     plot_average_choice, median_available, num_hist_bins,
                                     exclude_constant_angle=False,
                                     calculate_histograms=False):
    from django.db.models import Avg, Count, Min, Max, FloatField, When, Case, Sum, IntegerField
    from remapp.models import Median
    import numpy as np

    return_structure = {}

    if plot_average or plot_freq:
        # Obtain a list of series names
        return_structure['series_names'] = list(database_events.values_list(db_series_names, flat=True).distinct()
                                                .order_by(db_series_names))

        if plot_series_per_system and plot_average:
            # Obtain a list of x-ray systems
            return_structure['system_list'] = list(database_events.values_list(db_display_name_relationship, flat=True)
                                                   .distinct().order_by(db_display_name_relationship))
        else:
            return_structure['system_list'] = ['All systems']

        return_structure['summary'] = []

        if median_available and plot_average_choice == 'both':

            if plot_series_per_system and plot_average:
                # Calculate the mean, median and frequency for each x-ray system

                for system in return_structure['system_list']:
                    if exclude_constant_angle:
                        # Exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            mean=Avg(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                    default=db_value_name, output_field=FloatField()
                                )
                            ) * value_multiplier,
                            median=Median(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                    default=db_value_name, output_field=FloatField()
                                )
                            ) * value_multiplier,
                            num=Sum(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                    default=1, output_field=IntegerField()
                                )
                            )
                        ).order_by(db_series_names))
                    else:
                        # Don't exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            mean=Avg(db_value_name) * value_multiplier,
                            median=Median(db_value_name) * value_multiplier,
                            num=Count(db_value_name)).order_by(db_series_names))

            elif plot_average:
                # Calculate the mean, median and frequency for all data combined

                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        mean=Avg(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                default=db_value_name, output_field=FloatField()
                            )
                        ) * value_multiplier,
                        median=Median(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                default=db_value_name, output_field=FloatField()
                            )
                        ) * value_multiplier,
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        mean=Avg(db_value_name) * value_multiplier,
                        median=Median(db_value_name) * value_multiplier,
                        num=Count(db_value_name)).order_by(db_series_names))

            else:
                # Just calculate frequency of each series
                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Count(db_value_name)).order_by(db_series_names))

        elif median_available and plot_average_choice == 'median':

            if plot_series_per_system and plot_average:
                # Calculate the median and frequency for each x-ray system

                for system in return_structure['system_list']:
                    if exclude_constant_angle:
                        # Exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            median=Median(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                    default=db_value_name, output_field=FloatField()
                                )
                            ) * value_multiplier,
                            num=Sum(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                    default=1, output_field=IntegerField()
                                )
                            )
                        ).order_by(db_series_names))
                    else:
                        # Don't exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            median=Median(db_value_name) * value_multiplier,
                            num=Count(db_value_name)).order_by(db_series_names))

            elif plot_average:
                # Calculate the median and frequency for all data combined

                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        median=Median(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                default=db_value_name, output_field=FloatField()
                            )
                        ) * value_multiplier,
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        median=Median(db_value_name) * value_multiplier,
                        num=Count(db_value_name)).order_by(db_series_names))

            else:
                # Just calculate frequency of each series
                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Count(db_value_name)).order_by(db_series_names))

        else:

            if plot_series_per_system and plot_average:
                # Calculate the mean and frequency for each x-ray system

                for system in return_structure['system_list']:
                    if exclude_constant_angle:
                        # Exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            mean=Avg(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                    default=db_value_name, output_field=FloatField()
                                )
                            ) * value_multiplier,
                            num=Sum(
                                Case(
                                    When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                    default=1, output_field=IntegerField()
                                )
                            )
                        ).order_by(db_series_names))
                    else:
                        # Don't exclude "Constant Angle Acquisitions" from the calculations
                        return_structure['summary'].append(database_events.filter(
                            **{db_display_name_relationship: system}).values(db_series_names).annotate(
                            mean=Avg(db_value_name) * value_multiplier,
                            num=Count(db_value_name)).order_by(db_series_names))

            elif plot_average:
                # Calculate the mean and frequency for all data combined

                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        mean=Avg(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                                default=db_value_name, output_field=FloatField()
                            )
                        ) * value_multiplier,
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        mean=Avg(db_value_name) * value_multiplier,
                        num=Count(db_value_name)).order_by(db_series_names))

            else:
                # Just calculate frequency of each series
                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Sum(
                            Case(
                                When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=0),
                                default=1, output_field=IntegerField()
                            )
                        )
                    ).order_by(db_series_names))
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    return_structure['summary'].append(database_events.values(db_series_names).annotate(
                        num=Count(db_value_name)).order_by(db_series_names))

        # Force each item in return_structure['summary'] to be a list
        for index in range(len(return_structure['summary'])):
            return_structure['summary'][index] = list(return_structure['summary'][index])

        # Fill in default values where data for a series name is missing for any of the systems
        if plot_series_per_system and plot_average:
            for index in range(len(return_structure['system_list'])):
                missing_names =\
                    list(set(return_structure['series_names']) -
                         set([d[db_series_names] for d in return_structure['summary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['summary'][index]).append(
                            {'median': 0, 'mean': 0, db_series_names: missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['summary'][index]).append(
                            {'median': 0, db_series_names: missing_name, 'num': 0})
                    else:
                        (return_structure['summary'][index]).append(
                            {'mean': 0, db_series_names: missing_name, 'num': 0})
                # Rearrange the list into the same order as series_names
                summary_temp = []
                for series_name in return_structure['series_names']:
                    summary_temp.append(filter(lambda item: item[db_series_names] == series_name,
                                               return_structure['summary'][index])[0])
                return_structure['summary'][index] = summary_temp

    if plot_average and calculate_histograms:
        # Calculate histogram data for each series from each system
        return_structure['histogram_data'] =\
            [[[None for k in xrange(2)] for j in xrange(len(return_structure['series_names']))]
             for i in xrange(len(return_structure['system_list']))]

        if exclude_constant_angle:
            # Exclude "Constant Angle Acquisitions" from the calculations
            value_ranges = database_events.values(db_series_names).annotate(
                min_value=Min(
                    Case(
                        When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                        default=db_value_name, output_field=FloatField()
                    )
                ),
                max_value=Max(
                    Case(
                        When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                        default=db_value_name, output_field=FloatField()
                    )
                )
            ).order_by(db_series_names)
        else:
            # Don't exclude "Constant Angle Acquisitions" from the calculations
            value_ranges = database_events.values(db_series_names).annotate(
                    min_value=Min(db_value_name, output_field=FloatField()),
                    max_value=Max(db_value_name, output_field=FloatField())).order_by(db_series_names)

        for system_i, system in enumerate(return_structure['system_list']):
            for series_i, series_name in enumerate(return_structure['series_names']):
                if plot_series_per_system:
                    subqs = database_events.filter(**{
                            db_display_name_relationship: system,
                            db_series_names: series_name})
                else:
                    subqs = database_events.filter(**{db_series_names: series_name})

                if exclude_constant_angle:
                    # Exclude "Constant Angle Acquisitions" from the calculations
                    data_values = subqs.annotate(
                        values=Case(
                            When(ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition', then=None),
                            default=db_value_name, output_field=FloatField()
                        ),
                    ).values_list('values', flat=True)
                else:
                    # Don't exclude "Constant Angle Acquisitions" from the calculations
                    data_values = subqs.values_list(db_value_name, flat=True)

                if None in value_ranges.values_list('min_value', 'max_value')[series_i]:
                    return_structure['histogram_data'][system_i][series_i][0] = [0] * num_hist_bins
                    return_structure['histogram_data'][system_i][series_i][1] = [0] * (num_hist_bins+1)
                else:
                    return_structure['histogram_data'][system_i][series_i][0], \
                        return_structure['histogram_data'][system_i][series_i][1] = \
                        np.histogram([floatIfValueNone(x) for x in data_values], bins=num_hist_bins, range=value_ranges.values_list('min_value', 'max_value')[series_i])

                    return_structure['histogram_data'][system_i][series_i][0] = \
                        return_structure['histogram_data'][system_i][series_i][0].tolist()

                    return_structure['histogram_data'][system_i][series_i][1] = \
                        (return_structure['histogram_data'][system_i][series_i][1] * value_multiplier).tolist()

    return return_structure


def average_chart_over_time_data(database_events, db_series_names, db_value_name, db_date_field, db_date_time_field,
                                 median_available, plot_average_choice, value_multiplier, time_period):
    import datetime
    import qsstats
    from django.db.models import Min, Avg
    from remapp.models import Median

    return_structure = dict()

    return_structure['series_names'] = list(database_events.values_list(
        db_series_names, flat=True).distinct().order_by(db_series_names))

    start_date = database_events.aggregate(Min(db_date_field)).get(db_date_field+'__min')
    today = datetime.date.today()

    if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
        return_structure['median_over_time'] = [None] * len(return_structure['series_names'])
    if plot_average_choice == 'mean' or plot_average_choice == 'both':
        return_structure['mean_over_time'] = [None] * len(return_structure['series_names'])

    for i, series_name in enumerate(return_structure['series_names']):
        subqs = database_events.filter(**{db_series_names: series_name})

        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            qss = qsstats.QuerySetStats(subqs, db_date_time_field, aggregate=Avg(db_value_name) * value_multiplier)
            return_structure['mean_over_time'][i] = qss.time_series(start_date, today, interval=time_period)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            qss = qsstats.QuerySetStats(subqs, db_date_time_field, aggregate=Median(db_value_name) * value_multiplier)
            return_structure['median_over_time'][i] = qss.time_series(start_date, today, interval=time_period)

    return return_structure


def workload_chart_data(database_events):
    import datetime
    import qsstats

    return_structure = dict()

    return_structure['workload'] = [[0 for x in range(24)] for x in range(7)]
    for day in range(7):
        study_times_on_this_weekday = database_events.filter(study_date__week_day=day + 1).values(
            'study_workload_chart_time')

        if study_times_on_this_weekday:
            qss = qsstats.QuerySetStats(study_times_on_this_weekday, 'study_workload_chart_time')
            hourly_breakdown = qss.time_series(datetime.datetime(1900, 1, 1, 0, 0),
                                               datetime.datetime(1900, 1, 1, 23, 59), interval='hours')
            for hour in range(24):
                return_structure['workload'][day][hour] = hourly_breakdown[hour][1]

    return return_structure


def scatter_plot_data(database_events, x_field, y_field, plot_series_per_system, db_display_name_relationship):
    return_structure = dict()

    if plot_series_per_system:
        return_structure['system_list'] = list(database_events.values_list(db_display_name_relationship, flat=True)
                                               .distinct().order_by(db_display_name_relationship))
    else:
        return_structure['system_list'] = ['All systems']

    return_structure['scatterData'] = []
    if plot_series_per_system:
        for system in return_structure['system_list']:
            return_structure['scatterData'].append(database_events.filter(
                **{db_display_name_relationship: system}).values_list(x_field, y_field))
    else:
        return_structure['scatterData'].append(database_events.values_list(x_field, y_field))

    for index in range(len(return_structure['scatterData'])):
        return_structure['scatterData'][index] = [[floatIfValue(i[0]), floatIfValue(i[1])] for i in return_structure['scatterData'][index]]

    import numpy as np
    max_data = [0, 0]
    for index in range(len(return_structure['scatterData'])):
        current_max = np.amax(return_structure['scatterData'][index], 0).tolist()
        if current_max[0] > max_data[0]: max_data[0] = current_max[0]
        if current_max[1] > max_data[1]: max_data[1] = current_max[1]
    return_structure['maxXandY'] = max_data

    return return_structure


def floatIfValue(val):
    import numbers
    return float(val) if isinstance(val, numbers.Number) else 0.0


def floatIfValueNone(val):
    import numbers
    return float(val) if isinstance(val, numbers.Number) else None
