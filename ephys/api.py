from tastypie import fields
from ephys.models import *
from rest.resource import BaseMeta, BaseGNodeResource, BaseFileResourceMixin
from permissions.resource import PermissionsResourceMixin
from metadata.api import SectionResource


class BlockResource(BaseGNodeResource, PermissionsResourceMixin):
    metadata = fields.ToOneField(SectionResource, 'metadata', blank=True, null=True)
    segment_set = fields.ToManyField(
        'ephys.api.SegmentResource', 'segment_set', related_name='block',
        full=False, blank=True, null=True
    )
    recordingchannelgroup_set = fields.ToManyField(
        'ephys.api.RCGResource', 'recordingchannelgroup_set',
        related_name='block', full=False, blank=True, null=True
    )

    class Meta(BaseMeta):
        queryset = Block.objects.all()
        resource_name = Block.__name__.lower()


class SegmentResource(BaseGNodeResource):
    metadata = fields.ToOneField(SectionResource, 'metadata', blank=True, null=True)
    block = fields.ToOneField(BlockResource, 'block')
    spiketrain_set = fields.ToManyField(
        'ephys.api.SpikeTrainResource', 'spiketrain_set',
        related_name='segment', full=False, blank=True, null=True
    )
    spike_set = fields.ToManyField(
        'ephys.api.SpikeResource', 'spike_set',
        related_name='segment', full=False, blank=True, null=True
    )
    irregularlysampledsignal_set = fields.ToManyField(
        'ephys.api.IRSAResource', 'irregularlysampledsignal_set',
        related_name='segment', full=False, blank=True, null=True
    )
    analogsignal_set = fields.ToManyField(
        'ephys.api.AnalogSignalResource', 'analogsignal_set',
        related_name='segment', full=False, blank=True, null=True
    )
    analogsignalarray_set = fields.ToManyField(
        'ephys.api.ASAResource', 'analogsignalarray_set',
        related_name='segment', full=False, blank=True, null=True
    )
    event_set = fields.ToManyField(
        'ephys.api.EventResource', 'event_set',
        related_name='segment', full=False, blank=True, null=True
    )
    eventarray_set = fields.ToManyField(
        'ephys.api.EventArrayResource', 'eventarray_set',
        related_name='segment', full=False, blank=True, null=True
    )
    epoch_set = fields.ToManyField(
        'ephys.api.EpochResource', 'epoch_set',
        related_name='segment', full=False, blank=True, null=True
    )
    epocharray_set = fields.ToManyField(
        'ephys.api.EpochArrayResource', 'epocharray_set',
        related_name='segment', full=False, blank=True, null=True
    )

    class Meta(BaseMeta):
        queryset = Segment.objects.all()
        resource_name = Segment.__name__.lower()


class EventArrayResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')

    class Meta(BaseMeta):
        queryset = EventArray.objects.all()
        resource_name = EventArray.__name__.lower()


class EventResource(BaseGNodeResource):
    segment = fields.ToOneField(SegmentResource, 'segment')

    class Meta(BaseMeta):
        queryset = Event.objects.all()
        resource_name = Event.__name__.lower()


class EpochArrayResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')

    class Meta(BaseMeta):
        queryset = EpochArray.objects.all()
        resource_name = EpochArray.__name__.lower()


class EpochResource(BaseGNodeResource):
    segment = fields.ToOneField(SegmentResource, 'segment')

    class Meta(BaseMeta):
        queryset = Epoch.objects.all()
        resource_name = Epoch.__name__.lower()


class RCGResource(BaseGNodeResource):
    block = fields.ToOneField(BlockResource, 'block')
    unit_set = fields.ToManyField(
        'ephys.api.UnitResource', 'unit_set',
        related_name='recordingchannelgroup', full=False, blank=True, null=True
    )
    analogsignalarray_set = fields.ToManyField(
        'ephys.api.ASAResource', 'analogsignalarray_set',
        related_name='recordingchannelgroup', full=False, blank=True, null=True
    )

    class Meta(BaseMeta):
        queryset = RecordingChannelGroup.objects.all()
        resource_name = RecordingChannelGroup.__name__.lower()


class RCResource(BaseGNodeResource):

    # FIXME: m2m relationship does not work

    recordingchannelgroup = fields.ToManyField(
        'ephys.api.RCGResource', 'recordingchannelgroup',
        related_name='recordingchannel', full=False, blank=True, null=True
    )
    analogsignal_set = fields.ToManyField(
        'ephys.api.AnalogSignalResource', 'analogsignal_set',
        related_name='recordingchannel', full=False, blank=True, null=True
    )
    irregularlysampledsignal_set = fields.ToManyField(
        'ephys.api.IRSAResource', 'irregularlysampledsignal_set',
        related_name='recordingchannel', full=False, blank=True, null=True
    )

    class Meta(BaseMeta):
        queryset = RecordingChannel.objects.all()
        resource_name = RecordingChannel.__name__.lower()

    def hydrate_recordingchannelgroup(self, bundle):
        if bundle.obj.block_id is not None:
            return bundle

        if not 'recordingchannelgroup' in bundle.data.keys() or \
                len(bundle.data['recordingchannelgroup']) == 0:
            raise ValueError("'recordingchannelgroup' attribute is mandatory")

        rcg_field = self.fields['recordingchannelgroup']
        rcg_uri = bundle.data['recordingchannelgroup'][0]
        rcg = rcg_field.to_class().get_via_uri(rcg_uri, request=bundle.request)

        bundle.obj.block_id = rcg.block_id
        return bundle


class UnitResource(BaseGNodeResource):
    recordingchannelgroup = fields.ToOneField(RCGResource, 'recordingchannelgroup')
    spiketrain_set = fields.ToManyField(
        'ephys.api.SpikeTrainResource', 'spiketrain_set',
        related_name='unit', full=False, blank=True, null=True
    )
    spike_set = fields.ToManyField(
        'ephys.api.SpikeResource', 'spike_set',
        related_name='unit', full=False, blank=True, null=True
    )

    class Meta(BaseMeta):
        queryset = Unit.objects.all()
        resource_name = Unit.__name__.lower()


class SpikeTrainResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')
    unit = fields.ToOneField(UnitResource, 'unit')

    class Meta(BaseMeta):
        queryset = SpikeTrain.objects.all()
        resource_name = SpikeTrain.__name__.lower()


class ASAResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')
    recordingchannelgroup = fields.ToOneField(RCGResource, 'recordingchannelgroup')

    class Meta(BaseMeta):
        queryset = AnalogSignalArray.objects.all()
        resource_name = AnalogSignalArray.__name__.lower()


class AnalogSignalResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')
    recordingchannel = fields.ToOneField(RCResource, 'recordingchannel')

    class Meta(BaseMeta):
        queryset = AnalogSignal.objects.all()
        resource_name = AnalogSignal.__name__.lower()


class IRSAResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')
    recordingchannel = fields.ToOneField(RCResource, 'recordingchannel')

    class Meta(BaseMeta):
        queryset = IrregularlySampledSignal.objects.all()
        resource_name = IrregularlySampledSignal.__name__.lower()


class SpikeResource(BaseGNodeResource, BaseFileResourceMixin):
    segment = fields.ToOneField(SegmentResource, 'segment')
    unit = fields.ToOneField(UnitResource, 'unit')

    class Meta(BaseMeta):
        queryset = Spike.objects.all()
        resource_name = Spike.__name__.lower()